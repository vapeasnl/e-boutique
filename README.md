# E-Boutique

E-Boutique is an online store platform built with Flask, offering a range of features including product variations, advanced search and filters, product comparison, enhanced wishlist management, ratings and reviews, and recommendations.

## Features

- **Product Variations**: Manage different variations of products.
- **Advanced Search and Filters**: Perform advanced searches with multiple filters.
- **Product Comparison**: Compare different products.
- **Enhanced Wishlist Management**: Share and manage wishlists.
- **Ratings and Reviews**: Allow users to rate and review products.
- **Recommendations**: Provide product recommendations based on user preferences.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/vapeasnl/e-boutique.git
    cd e-boutique
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Configuration

- Ensure to set up your environment variables for database connection, secret key, etc., in a `.env` file.

## Usage

- Navigate to `http://127.0.0.1:5000` in your browser to access the application.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
