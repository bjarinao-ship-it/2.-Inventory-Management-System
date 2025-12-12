const API_BASE = 'http://localhost:5000';

// Load products and stock value on page load
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    loadStockValue();
});

// Load all products
async function loadProducts() {
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const productsList = document.getElementById('productsList');
    
    loading.style.display = 'block';
    errorDiv.style.display = 'none';
    productsList.innerHTML = '';

    try {
        const response = await fetch(`${API_BASE}/products/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const products = await response.json();
        loading.style.display = 'none';

        if (products.length === 0) {
            productsList.innerHTML = `
                <div class="empty-state">
                    <p>📭 No products found</p>
                    <p>Add your first product using the form on the left!</p>
                </div>
            `;
            return;
        }

        productsList.innerHTML = products.map(product => `
            <div class="product-card">
                <h3>${escapeHtml(product.name)}</h3>
                <div class="product-info">
                    <p><strong>Price:</strong> $${parseFloat(product.price).toFixed(2)}</p>
                    <p><strong>Quantity:</strong> ${product.quantity}</p>
                    <p><strong>Total Value:</strong> $${(parseFloat(product.price) * parseInt(product.quantity)).toFixed(2)}</p>
                </div>
                <div class="product-actions">
                    <button class="btn-edit" onclick="editProduct(${product.id}, '${escapeHtml(product.name)}', ${product.price}, ${product.quantity})">
                        Edit
                    </button>
                    <button class="btn-delete" onclick="deleteProduct(${product.id})">
                        Delete
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        loading.style.display = 'none';
        errorDiv.style.display = 'block';
        errorDiv.textContent = `Error loading products: ${error.message}`;
        console.error('Error:', error);
    }
}

// Load total stock value
async function loadStockValue() {
    try {
        const response = await fetch(`${API_BASE}/reports/stock-value`);
        if (response.ok) {
            const data = await response.json();
            document.getElementById('totalValue').textContent = parseFloat(data.total_stock_value).toFixed(2);
        }
    } catch (error) {
        console.error('Error loading stock value:', error);
    }
}

// Handle form submission
document.getElementById('productForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const productId = document.getElementById('productId').value;
    const name = document.getElementById('productName').value;
    const price = parseFloat(document.getElementById('productPrice').value);
    const quantity = parseInt(document.getElementById('productQuantity').value);

    try {
        let response;
        if (productId) {
            // Update existing product
            response = await fetch(`${API_BASE}/products/update/${productId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, price, quantity })
            });
        } else {
            // Add new product
            response = await fetch(`${API_BASE}/products/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, price, quantity })
            });
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to save product');
        }

        // Success
        resetForm();
        loadProducts();
        loadStockValue();
        alert(productId ? 'Product updated successfully!' : 'Product added successfully!');
    } catch (error) {
        alert(`Error: ${error.message}`);
        console.error('Error:', error);
    }
});

// Edit product
function editProduct(id, name, price, quantity) {
    document.getElementById('productId').value = id;
    document.getElementById('productName').value = name;
    document.getElementById('productPrice').value = price;
    document.getElementById('productQuantity').value = quantity;
    document.getElementById('formTitle').textContent = 'Edit Product';
    document.getElementById('submitBtn').textContent = 'Update Product';
    document.getElementById('cancelBtn').style.display = 'block';
    
    // Scroll to form
    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
}

// Delete product
async function deleteProduct(id) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/products/delete/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to delete product');
        }

        loadProducts();
        loadStockValue();
        alert('Product deleted successfully!');
    } catch (error) {
        alert(`Error: ${error.message}`);
        console.error('Error:', error);
    }
}

// Reset form
function resetForm() {
    document.getElementById('productForm').reset();
    document.getElementById('productId').value = '';
    document.getElementById('formTitle').textContent = 'Add New Product';
    document.getElementById('submitBtn').textContent = 'Add Product';
    document.getElementById('cancelBtn').style.display = 'none';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
