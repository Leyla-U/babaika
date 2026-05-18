const Stripe = require('stripe');
const nodemailer = require('nodemailer');

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.GMAIL_USER || 'babaika.objects@gmail.com',
    pass: process.env.GMAIL_PASS || process.env.GMAIL_APP_PASSWORD || 'dopa cahc lvyt zsop',
  },
});

// Vercel needs this to not parse the body so Stripe can verify the signature
const config = {
  api: {
    bodyParser: false,
  },
};

// Helper to read the raw body for signature verification
async function getRawBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(typeof chunk === 'string' ? Buffer.from(chunk) : chunk);
  }
  return Buffer.concat(chunks);
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).end('Method Not Allowed');
  }

  let event;
  const signature = req.headers['stripe-signature'];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  try {
    const rawBody = await getRawBody(req);
    event = stripe.webhooks.constructEvent(rawBody, signature, webhookSecret);
  } catch (err) {
    console.error(`Webhook Error: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Look for a successful checkout payment
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    
    const customerName = session.customer_details?.name || 'Customer';
    const customerEmail = session.customer_details?.email;

    // 1. Grab the custom notes from the checkout fields/metadata
    // We previously saved this in the metadata as 'customer_notes'
    const sizingNotes = session.metadata?.customer_notes || 'None requested — standard sizing will be crafted.';

    if (customerEmail) {
      try {
        // 2. Send the automated production start email
        await transporter.sendMail({
          from: `"Babaika Studio" <${process.env.GMAIL_USER || 'babaika.objects@gmail.com'}>`,
          to: customerEmail,
          subject: 'Your Babaika piece is now in production',
          html: `
            <div style="font-family: sans-serif; max-width: 600px; color: #222; line-height: 1.6;">
              <h2 style="font-weight: normal; border-bottom: 1px solid #eee; padding-bottom: 10px;">Thank you for supporting independent craft.</h2>
              <p>Hi ${customerName},</p>
              <p>Your payment has been successfully confirmed, and the studio has officially begun crafting your order.</p>
              <p>Because every Babaika object is individually handmade to order here in Mexico City, <strong>please allow approximately 2 weeks for the creation, finishing, and packaging of your pieces.</strong> We believe slow, intentional production makes for objects worth waiting for.</p>
              
              <div style="background-color: #f9f9f9; padding: 15px; margin: 20px 0; border-radius: 4px; border-left: 3px solid #000;">
                <h4 style="margin-top: 0; margin-bottom: 5px;">Custom Adaptations & Notes:</h4>
                <p style="font-style: italic; color: #555; margin: 0;">"${sizingNotes}"</p>
              </div>
              
              <p>We will send you a tracking number the exact moment your package is packed and dispatched from the studio.</p>
              <br />
              <p>With care,<br /><strong>Babaika Studio</strong></p>
            </div>
          `,
        });
        console.log(`Production email successfully sent to ${customerEmail}`);
      } catch (emailError) {
        console.error('Nodemailer error:', emailError);
      }
    }
  }

  return res.status(200).json({ received: true });
}

module.exports.config = config;
