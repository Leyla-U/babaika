import { NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export async function POST(request) {
  try {
    const { items } = await request.json();
    // items: [{ priceId: string, quantity: number }]

    if (!items || items.length === 0) {
      return NextResponse.json({ error: 'No items in cart' }, { status: 400 });
    }

    const line_items = items.map(item => ({
      price: item.priceId,
      quantity: item.quantity || 1,
    }));

    const session = await stripe.checkout.sessions.create({
      line_items,
      mode: 'payment',
      shipping_address_collection: {
        allowed_countries: ['MX', 'US', 'CA', 'GB', 'DE', 'FR', 'ES', 'IT', 'NL', 'AU', 'JP', 'KR', 'RU', 'KZ'],
      },
      success_url: `${request.headers.get('origin')}/catalogue.html?order=success`,
      cancel_url: `${request.headers.get('origin')}/catalogue.html`,
    });

    return NextResponse.json({ url: session.url });
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
