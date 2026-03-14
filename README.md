# 🚩 PunjabiLang (ਪੰਜਾਬੀ ਲੈਂਗੂਏਜ)

**PunjabiLang** is a localized, high-level, interpreted programming language designed to make coding accessible using Romanized Punjabi syntax. 

## 🚀 Features

* **Localized Syntax**: Use familiar terms like `manno`, `je`, and `kamm`.
* **Modular Design**: Standard library support via `shaamil`.
* **Data Structures**: Full support for Arrays `[]` and Dictionaries `{}`.
* **File I/O**: Built-in functions to `kholo`, `parho`, and `likho_file`.
* **Smart Built-ins**: Includes `ganit`, `ank`, `tuka`, and `samaa`.
* **Error Handling**: Professional reporting with specific line numbers.

---

## 🛠️ Installation & Setup

### 1. Setup Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Build the Standalone Compiler

```
pip install pyinstaller
python -m pyinstaller --onefile --name punjabi main.py
```

## 💻 Example Code (bujho.pj)

```
manno sahi_jawab = tuka(1, 10);
likh("1 ton 10 de vitch ek number bujho!");

manno jittya = 0;
jadon_takk (jittya == 0) {
    likh("Tuhada tuka ki hai?");
    manno tuka_user = ank(bhar());
    
    je (tuka_user == sahi_jawab) {
        likh("Sahi jawab! Tusi jitt gaye!");
        jittya = 1;
    } nahi_taan {
        likh("Galat! Dobara koshish karo.");
    }
}
```

## 📂 Project Structure
```
src/lexer.py: Tokenizer.

src/parser.py: AST Builder.

src/ast.py: Language Nodes.

src/evaluator.py: Execution Engine.

src/environment.py: Memory Management.
```