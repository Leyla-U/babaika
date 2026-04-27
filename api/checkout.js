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
    const { items } = req.body;

    if (!items || items.length === 0) {
      return res.status(400).json({ error: 'No items in cart' });
    }

    const line_items = items.map(item => ({
      price: item.priceId,
      quantity: item.quantity || 1,
    }));

    const origin = req.headers.origin || `https://${req.headers.host}`;

    const session = await stripe.checkout.sessions.create({
      line_items,
      mode: 'payment',
      shipping_address_collection: {
        allowed_countries: ['MX', 'US', 'CA', 'GB', 'DE', 'FR', 'ES', 'IT', 'NL', 'AU', 'JP', 'KR', 'RU', 'KZ'],
      },
      success_url: `${origin}/catalogue.html?order=success`,
      cancel_url:  `${origin}/catalogue.html`,
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Stripe error:', err.message);
    return res.status(500).json({ error: err.message });
  }
};
