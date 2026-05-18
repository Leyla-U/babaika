const Stripe = require('stripe');

module.exports = async function handler(req, res) {
  // Only accept POST
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
  if (!stripeSecretKey) {
    return res.status(500).json({ error: 'Stripe secret key not configured.' });
  }

  const stripe = new Stripe(stripeSecretKey);

  try {
    const { items, notes } = req.body;

    if (!items || items.length === 0) {
      return res.status(400).json({ error: 'No items in cart' });
    }

    const line_items = items.map(item => ({
      price: item.priceId,
      quantity: item.quantity || 1,
    }));

    const origin = req.headers.origin || `https://${req.headers.host}`;

    const sessionParams = {
      line_items,
      mode: 'payment',
      billing_address_collection: 'required',
      customer_creation: 'always',
      // Shipping options — customer selects at checkout
      shipping_options: [
        { shipping_rate: 'shr_1TYI7tJPn6LmQgwJOD7VGgJk' }, // Mexico City (Free)
        { shipping_rate: 'shr_1TYFbWJPn6LmQgwJysioBAaa' }, // Domestic (MX)
        { shipping_rate: 'shr_1TYFbkJPn6LmQgwJSOQfWURp' }, // International — US & Canada
        { shipping_rate: 'shr_1TYFdOJPn6LmQgwJjEFHW9WD' }, // International — Rest of World
      ],
      // Stripe collects the shipping address automatically when shipping_options is set
      shipping_address_collection: {
        allowed_countries: ['MX', 'US', 'CA', 'GB', 'DE', 'FR', 'ES', 'IT', 'NL', 'AU', 'JP', 'KR', 'RU', 'KZ'],
      },
      payment_intent_data: {},
      success_url: `${origin}/success.html`,
      cancel_url:  `${origin}/catalogue.html`,
    };

    // Attach customer notes to session metadata if provided
    if (notes && notes.trim()) {
      sessionParams.metadata = { customer_notes: notes.trim().substring(0, 500) };
      sessionParams.payment_intent_data = {
        ...sessionParams.payment_intent_data,
        metadata: { customer_notes: notes.trim().substring(0, 500) },
      };
    }

    const session = await stripe.checkout.sessions.create(sessionParams);

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Stripe error:', err.message);
    return res.status(500).json({ error: err.message });
  }
};
