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
        // Retrieve line items to show in the email
        const lineItems = await stripe.checkout.sessions.listLineItems(session.id);
        const orderDetails = lineItems.data.map(item => `- ${item.description} (Qty: ${item.quantity})`).join('<br>');

        const address = session.shipping_details?.address;
        const shippingAddress = address 
          ? `${address.line1 || ''} ${address.line2 || ''}<br>${address.city || ''}, ${address.state || ''} ${address.postal_code || ''}<br>${address.country || ''}`
          : 'Address not provided at checkout.';

        // 2. Send the automated production start email
        await transporter.sendMail({
          from: `"Babaika Studio" <${process.env.GMAIL_USER || 'babaika.objects@gmail.com'}>`,
          to: customerEmail,
          subject: 'Order Confirmed: Babaika Archive.',
          html: `
            <div style="font-family: sans-serif; max-width: 600px; color: #222; line-height: 1.6;">
              <p>Your order has been securely received.</p>
              <p>Thank you for acquiring a piece of Volume 01. Because every artifact is prepared and finished by hand, your piece is currently undergoing manual processing in our studio.</p>
              
              <h4 style="margin-bottom: 5px;">Order Details:</h4>
              <p style="margin-top: 0;">${orderDetails}</p>

              <h4 style="margin-bottom: 5px;">Destination:</h4>
              <p style="margin-top: 0;">${shippingAddress}</p>

              <div style="background-color: #f9f9f9; padding: 15px; margin: 20px 0; border-radius: 4px; border-left: 3px solid #000;">
                <h4 style="margin-top: 0; margin-bottom: 5px;">Custom Adaptations & Notes:</h4>
                <p style="font-style: italic; color: #555; margin: 0;">"${sizingNotes}"</p>
              </div>
              
              <p>You will receive an update with tracking information the moment your package is ready to ship.</p>
              <br />
              <p>The Babaika Studio.</p>
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
