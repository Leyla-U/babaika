const nodemailer = require('nodemailer');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  // Set your gmail address here
  const gmailUser = process.env.GMAIL_USER || 'babaika.objects@gmail.com'; 
  const gmailPass = process.env.GMAIL_PASS || 'dopa cahc lvyt zsop';

  if (!gmailUser || !gmailPass) {
    return res.status(500).json({ error: 'Email configuration missing.' });
  }

  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: gmailUser,
      pass: gmailPass,
    },
  });

  try {
    const body = req.body || {};
    
    // Format the email content
    const htmlContent = `
      <h2>New Babaika Order Inquiry</h2>
      <p><strong>Name:</strong> ${body.name || 'N/A'}</p>
      <p><strong>Email:</strong> ${body.email || 'N/A'}</p>
      <p><strong>Country:</strong> ${body.country || 'N/A'}</p>
      <p><strong>Address:</strong> ${body.address || 'N/A'}</p>
      <p><strong>Size / Notes:</strong> ${body.sizes_and_notes || 'N/A'}</p>
      <br/>
      <h3>Order Details:</h3>
      <pre>${body.order_details || 'N/A'}</pre>
    `;

    const mailOptions = {
      from: gmailUser,
      to: gmailUser, // Send to yourself
      replyTo: body.email,
      subject: `New Inquiry from ${body.name || 'Babaika Customer'}`,
      html: htmlContent,
    };

    await transporter.sendMail(mailOptions);
    
    // If it's a standard form submission (application/x-www-form-urlencoded), redirect.
    // If it's a fetch request (application/json), return JSON.
    const contentType = req.headers['content-type'] || '';
    if (contentType.includes('application/json')) {
      return res.status(200).json({ success: true });
    } else {
      // Redirect to the success page on traditional form submit
      const origin = req.headers.origin || `https://${req.headers.host}`;
      return res.redirect(302, `${origin}/success.html`);
    }

  } catch (error) {
    console.error('Email sending error:', error);
    return res.status(500).json({ error: 'Failed to send email.' });
  }
};
