# My Zootopia Project

Welcome to My Zootopia! This Python project allows you to fetch and display detailed information about various animals using the [API Ninjas](https://api-ninjas.com/api/animals) data service. The program will generate an HTML page that shows selected animals based on skin type and other characteristics.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Ell-716/My-Zootopia.git
    ```

2. **Set Up a Virtual Environment (optional but recommended):**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\\Scripts\\activate
    ```

3. **Install the required packages:**

    Make sure you have [Python](https://www.python.org/downloads/) installed. Once inside the project folder, run the following command to install all the necessary packages:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**

    Create a `.env` file in the root directory of the project and add your API key. You can obtain an API key from [API Ninjas](https://api-ninjas.com/api/animals):

    ```plaintext
    API_KEY=your_api_key_here
    ```

## Usage

1. **Run the program:**

    Once everything is set up, run the Python script using:

    ```bash
    python main.py
    ```

2. **Interact with the program:**

    After running the program, you'll be prompted to enter the name of an animal (e.g., "elephant"). The program will fetch and display information such as the animal's diet, lifespan, skin type, and more. It will then generate an HTML file displaying the animal details.

3. **Example:**

    If you input "elephant", the program will retrieve elephant-related data, including its skin type and characteristics, and display this information in an HTML page.

## Contributing

Contributions are welcome! If you wish to improve this project, feel free to follow these steps:

1. **Fork the repository** by clicking on the "Fork" button in GitHub.
2. **Create a new branch** with a descriptive name for your feature:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes** and commit them with a meaningful message:
    ```bash
    git commit -m "Add feature X"
    ```
4. **Push your branch** to your forked repository:
    ```bash
    git push origin feature/your-feature-name
    ```
5. **Create a Pull Request** and submit it to discuss the changes.


## Acknowledgments

Thanks to [API Ninjas](https://api-ninjas.com/api/animals) for providing the animal data API.
