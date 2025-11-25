# NetCart Checkout - Product Specifications

## Products Available
1. **Wireless Earbuds** - Acme Audio Co. - $49.99
2. **Smart Watch** - ChronoTech - $79.99
3. **Portable Speaker** - SoundWave - $29.99

## Discount Coupon System

### Valid Coupons
- **SAVE15**: Applies 15% discount to subtotal
  - Must be entered in coupon field (id="coupon")
  - Click "Apply" button to activate
  - Discount shown in cart total
  
- **WELCOME10**: Applies 10% discount for new customers
  - Same application process as SAVE15

### Coupon Rules
- Only one coupon per order
- Coupons are case-insensitive (save15 = SAVE15)
- Invalid coupons display error message
- Coupon applies to subtotal before shipping

## Shipping Options

### Standard Shipping
- **Cost**: Free
- **Delivery**: 5-7 business days
- **Radio button**: id="ship-standard"
- **Default**: Selected by default

### Express Shipping
- **Cost**: $10 additional
- **Delivery**: 1-2 business days
- **Radio button**: id="ship-express"
- **Display**: Shows "Express ($10)" in UI

## Payment Methods

### Credit / Debit Card
- **Radio button**: id="pay-card"
- **Default**: Selected by default
- **Input field**: id="card-number"
- **Accepted**: Visa, MasterCard, American Express
- **Placeholder**: "xxxx xxxx xxxx xxxx"

### PayPal (Simulated)
- **Radio button**: id="pay-paypal"
- **Behavior**: Shows note about simulation
- **Note**: "You will be redirected to PayPal (simulated for demo)"

### UPI
- **Radio button**: id="pay-upi"
- **Input field**: id="upi-id"
- **Placeholder**: "example@upi"
- **Note**: Demo only

## Cart Functionality

### Add to Cart
- Each product has "Add to Cart" button with class="btn-add"
- Button includes data-id attribute matching product
- Cart updates dynamically with JavaScript
- Cart items displayed in element id="cart-items"

### Cart Display
- **Subtotal**: id="subtotal" - Shows sum of all items
- **Shipping**: id="shipping" - Shows "Free" or "$10"
- **Total**: id="cart-total" - Final amount to pay
- Empty cart message: "Your cart is empty. Add items to begin."

## Form Validation

### Required Fields
- **Name**: id="name"
  - Minimum 2 characters
  - Error display: id="err-name"
  
- **Email**: id="email"
  - Must be valid email format
  - Type: email
  - Error display: id="err-email"
  
- **Address**: id="address"
  - Textarea element
  - Minimum 10 characters

### Validation Behavior
- Errors shown in red text
- Error elements have class="input-error"
- Initially hidden with class="hidden"
- Displayed when validation fails

## Success Criteria
- Payment success message: id="payment-result"
- Text: "Payment Successful! ✅"
- Initially hidden with class="hidden"
- Displayed after successful payment