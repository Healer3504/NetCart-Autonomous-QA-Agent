from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List

def parse_html_structure(html_path: str) -> Dict:
    """
    Parse YOUR Netflix checkout.html and extract all selectors.
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        selectors = {
            'buttons': [],
            'inputs': [],
            'product_cards': [],
            'cart_elements': []
        }
        
        # Extract Add to Cart buttons
        for btn in soup.find_all('button', class_='btn-add'):
            selectors['buttons'].append({
                'class': 'btn-add',
                'data-id': btn.get('data-id'),
                'purpose': 'add_to_cart'
            })
        
        # Extract Apply Coupon button
        apply_btn = soup.find('button', id='apply-coupon')
        if apply_btn:
            selectors['buttons'].append({
                'id': 'apply-coupon',
                'class': apply_btn.get('class'),
                'purpose': 'apply_coupon'
            })
        
        # Extract Pay Now button
        pay_btn = soup.find('button', id='pay-now')
        if pay_btn:
            selectors['buttons'].append({
                'id': 'pay-now',
                'class': pay_btn.get('class'),
                'purpose': 'payment'
            })
        
        # Extract View Cart button
        view_cart = soup.find('button', id='view-cart')
        if view_cart:
            selectors['buttons'].append({
                'id': 'view-cart',
                'purpose': 'view_cart'
            })
        
        # Extract input fields
        inputs_map = {
            'coupon': 'coupon code input',
            'name': 'customer name',
            'email': 'customer email',
            'address': 'shipping address',
            'card-number': 'card number',
            'upi-id': 'UPI ID'
        }
        
        for inp_id, purpose in inputs_map.items():
            inp = soup.find(attrs={'id': inp_id})
            if inp:
                selectors['inputs'].append({
                    'id': inp_id,
                    'name': inp.get('name'),
                    'type': inp.get('type') or inp.name,
                    'purpose': purpose
                })
        
        # Extract radio buttons
        for radio in soup.find_all('input', type='radio'):
            selectors['inputs'].append({
                'id': radio.get('id'),
                'name': radio.get('name'),
                'value': radio.get('value'),
                'type': 'radio',
                'purpose': f"{radio.get('name')} selection"
            })
        
        # Extract product cards
        for card in soup.find_all('div', class_='product-card'):
            selectors['product_cards'].append({
                'data-id': card.get('data-id'),
                'class': 'product-card'
            })
        
        # Extract cart elements
        cart_elements = ['cart-items', 'subtotal', 'shipping', 'cart-total']
        for elem_id in cart_elements:
            elem = soup.find(id=elem_id)
            if elem:
                selectors['cart_elements'].append({
                    'id': elem_id,
                    'purpose': elem_id.replace('-', ' ')
                })
        
        return {
            'selectors': selectors,
            'raw_html': html_content,
            'features': extract_features_from_html(soup)
        }
    
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return {'selectors': {}, 'raw_html': '', 'features': []}


def extract_features_from_html(soup: BeautifulSoup) -> List[str]:
    """Extract features present in the HTML"""
    features = []
    
    # Check for products
    products = soup.find_all('div', class_='product-card')
    if products:
        features.append(f"Product Catalog ({len(products)} products)")
    
    # Check for coupon
    if soup.find(id='coupon'):
        features.append("Discount Coupon System")
    
    # Check for shipping options
    if soup.find('input', attrs={'name': 'shipping'}):
        features.append("Shipping Method Selection")
    
    # Check for payment options
    payment_radios = soup.find_all('input', attrs={'name': 'payment'})
    if payment_radios:
        methods = [r.get('value') for r in payment_radios]
        features.append(f"Payment Methods: {', '.join(methods)}")
    
    # Check for form validation
    if soup.find_all('div', class_='input-error'):
        features.append("Form Validation")
    
    return features
