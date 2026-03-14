# 🤝 Contributing to PunjabiLang

First off, thank you for considering contributing to PunjabiLang! It's people like you that will make this language a powerful tool for the Punjabi-speaking community.

## 🌟 How Can You Help?

### 1. Suggesting New Keywords
We want the language to feel as natural as possible. If you think a keyword should be different or if we are missing a common Punjabi term for a programming concept, please open an "Issue."

### 2. Adding Built-in Functions
Do you want to add support for math (like `root()`) or string manipulation? 
* Look at `src/evaluator.py` under the `FunctionCall` block.
* Add your logic using Python's libraries.

### 3. Improving Documentation
If you find a typo in the README or want to add a new example script to the `examples/` folder, feel free to submit a Pull Request!

---

## 🛠️ Development Workflow

1. **Fork the Repo**: Create your own copy of the project.
2. **Create a Branch**: `git checkout -b feature/nava-feature`.
3. **Make Changes**: Ensure your code follows the existing structure in `src/`.
4. **Test Your Changes**: Run your new logic using `python main.py examples/test_script.pj`.
5. **Submit a Pull Request**: Explain what you changed and why it helps the language.

---

## 📜 Coding Guidelines
* Keep the core logic in `src/`.
* Use Punjabi for keywords but keep the internal Python variable names in English for technical clarity.
* Ensure every new feature has an example script in the `examples/` folder.

**Let's build the future of Punjabi programming together!**