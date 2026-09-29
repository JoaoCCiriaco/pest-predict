import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session importAqui tens o ficheiro **`app.py`** completo, limpo e corrigido para passar no `check50` sem lançar exceções na página de venda:

```python
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from
