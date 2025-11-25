// products & basic cart
const products = {
  p1: { id: 'p1', title: 'Wireless Earbuds', company: 'Acme Audio Co.', price: 49.99 },
  p2: { id: 'p2', title: 'Smart Watch', company: 'ChronoTech', price: 79.99 },
  p3: { id: 'p3', title: 'Portable Speaker', company: 'SoundWave', price: 29.99 }
};

let cart = {};
let lastAppliedCoupon = null;

function formatPrice(v) {
  return '$' + v.toFixed(2);
}

function calcSubtotal() {
  let subtotal = 0;
  for (const id in cart) {
    subtotal += products[id].price * cart[id];
  }
  return subtotal;
}

function renderCart() {
  const container = document.getElementById('cart-items');
  container.innerHTML = '';

  if (Object.keys(cart).length === 0) {
    container.innerHTML = '<div class="muted">Your cart is empty. Add items to begin.</div>';
  }

  for (const id in cart) {
    const item = products[id];
    const qty = cart[id];

    const row = document.createElement('div');
    row.className = 'cart-row';
    row.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;">
        <div>
          <div style="font-weight:700">${item.title}</div>
          <div style="font-size:12px;color:#9a9a9a">${item.company}</div>
        </div>
        <div style="text-align:right">
          <div>${formatPrice(item.price)}</div>
          <div style="margin-top:6px">Qty:
            <input class="qty" data-id="${id}" type="number" min="0" value="${qty}" style="width:60px;padding:6px;border-radius:6px;background:#0d0d0d;border:1px solid #232323;color:#fff" />
          </div>
        </div>
      </div>
    `;
    container.appendChild(row);
  }

  updateSummary();
}

function updateSummary() {
  const subtotal = calcSubtotal();
  const shipping = document.querySelector('input[name="shipping"]:checked').value;
  let total = subtotal;
  document.getElementById('subtotal').innerText = formatPrice(subtotal);

  if (shipping === 'express') {
    total += 10;
    document.getElementById('shipping').innerText = '$10.00';
  } else {
    document.getElementById('shipping').innerText = 'Free';
  }

  // apply coupon if present
  if (lastAppliedCoupon === 'SAVE15') {
    const discounted = parseFloat((total * 0.85).toFixed(2));
    document.getElementById('cart-total').innerText = formatPrice(discounted);
    // animate highlight
    const totalEl = document.getElementById('cart-total');
    totalEl.classList.add('coupon-applied');
    setTimeout(()=> totalEl.classList.remove('coupon-applied'), 900);
  } else {
    document.getElementById('cart-total').innerText = formatPrice(total);
  }
}

// Add to cart
document.querySelectorAll('.btn-add').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.dataset.id;
    cart[id] = (cart[id] || 0) + 1;
    renderCart();
  });
});

// Qty change
document.addEventListener('input', e => {
  if (e.target.classList.contains('qty')) {
    const id = e.target.dataset.id;
    const v = parseInt(e.target.value || '0');
    if (v <= 0) {
      delete cart[id];
    } else {
      cart[id] = v;
    }
    renderCart();
  }
});

// Shipping change
document.addEventListener('change', e => {
  if (e.target.name === 'shipping') {
    updateSummary();
  }
});

// Coupon apply
document.getElementById('apply-coupon').addEventListener('click', () => {
  const code = document.getElementById('coupon').value.trim().toUpperCase();
  if (!code) {
    alert('Enter a coupon code to apply.');
    return;
  }
  if (code === 'SAVE15') {
    lastAppliedCoupon = 'SAVE15';
    updateSummary();
    alert('Coupon applied: 15% OFF');
  } else {
    lastAppliedCoupon = null;
    updateSummary();
    alert('Invalid coupon');
  }
});

// Payment method toggle
function showPaymentFields() {
  const method = document.querySelector('input[name="payment"]:checked').value;
  const cardFields = document.getElementById('card-fields');
  const paypalNote = document.getElementById('paypal-note');
  const upiFields = document.getElementById('upi-fields');

  // Hide all then reveal the selected structured block
  cardFields.classList.toggle('hidden', method !== 'card');
  paypalNote.classList.toggle('hidden', method !== 'paypal');
  upiFields.classList.toggle('hidden', method !== 'upi');
}
document.querySelectorAll('input[name="payment"]').forEach(r => {
  r.addEventListener('change', showPaymentFields);
});
showPaymentFields(); // initialize on load

// Pay Now
document.getElementById('pay-now').addEventListener('click', () => {
  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  let ok = true;

  if (!name) {
    document.getElementById('err-name').innerText = 'Name required';
    document.getElementById('err-name').classList.remove('hidden');
    ok = false;
  } else {
    document.getElementById('err-name').classList.add('hidden');
  }

  const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailRe.test(email)) {
    document.getElementById('err-email').innerText = 'Valid email required';
    document.getElementById('err-email').classList.remove('hidden');
    ok = false;
  } else {
    document.getElementById('err-email').classList.add('hidden');
  }

  if (Object.keys(cart).length === 0) {
    alert('Cart is empty. Add items before checkout.');
    ok = false;
  }

  if (!ok) return;

  // Simulate payment behavior depending on method
  const method = document.querySelector('input[name="payment"]:checked').value;
  if (method === 'card') {
    // basic check for card number
    const cn = document.getElementById('card-number').value.trim();
    if (!cn || cn.length < 8) {
      alert('Enter a valid card number (demo).');
      return;
    }
  } else if (method === 'upi') {
    const upi = document.getElementById('upi-id').value.trim();
    if (!upi || !upi.includes('@')) {
      alert('Enter a valid UPI ID (e.g. example@upi).');
      return;
    }
  } // paypal requires no local validation for demo

  // show success
  const result = document.getElementById('payment-result');
  result.classList.remove('hidden');
  result.innerText = 'Payment Successful! ✅';

  // small confetti-like visual: pulse the success area
  result.animate([{ transform: 'scale(.98)', opacity: .9 }, { transform: 'scale(1)', opacity: 1 }], { duration: 320, easing: 'ease-out' });

  // after payment, keep cart but reset coupon visual
  lastAppliedCoupon = null;
  setTimeout(() => {
    // optional: reset cart after completion
    // cart = {}; renderCart();
  }, 1200);
});

// expose small API for Selenium / tests
window.__NETCART__ = {
  getCart: () => JSON.parse(JSON.stringify(cart)),
  reset: () => {
    cart = {};
    lastAppliedCoupon = null;
    renderCart();
    document.getElementById('coupon').value = '';
    document.getElementById('payment-result').classList.add('hidden');
    document.getElementById('card-number').value = '';
    document.getElementById('upi-id').value = '';
  }
};

// initial
renderCart();
