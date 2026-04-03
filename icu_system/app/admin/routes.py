from flask import Blueprint, abort, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import text

from ..extensions import db


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_TABLES = {'patient', 'vital_periodic', 'lab', 'medication', 'diagnosis', 'note', 'users'}


def admin_only():
    if current_user.role != 'admin':
        abort(403)


@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def admin_home():
    admin_only()

    table_name = request.args.get('table', 'patient')
    rows = []
    columns = []
    sql_result = None

    if table_name in ALLOWED_TABLES:
        result = db.session.execute(text(f'SELECT * FROM {table_name} LIMIT 20'))
        rows = result.fetchall()
        columns = result.keys()

    if request.method == 'POST':
        sql = request.form.get('sql', '').strip()
        if sql.lower().startswith('select'):
            result = db.session.execute(text(sql))
            sql_result = {
                'columns': result.keys(),
                'rows': result.fetchall(),
            }

    return render_template(
        'admin.html',
        table_name=table_name,
        allowed_tables=sorted(ALLOWED_TABLES),
        columns=columns,
        rows=rows,
        sql_result=sql_result,
    )
