from apps.home import blueprint
from flask import jsonify, render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask_login import (
    current_user,
    login_user,
    logout_user
)
import apps.blockchain.gradingchain as gc

blockchain = gc.Blockchain()

def display_chain():
    valid = blockchain.chain_valid(blockchain.chain)
    

    response = {
                'length': len(blockchain.chain),
                'valid': valid,
                'Grading Chain': blockchain.chain
                }
    return response



@blueprint.route('/index')
@login_required
def index():
    if current_user.role == 99:
        return render_template('home/admin-index.html', segment='index', chain = display_chain(), lc = len(blockchain.chain), bc = blockchain.chain)
    return render_template('home/admin-index.html', segment='index', chain = display_chain(), lc = len(blockchain.chain), bc = blockchain.chain)

@blueprint.route('/show_grades', methods=['GET', 'POST'])
@login_required
def showg():
    if current_user.role == 99:
        
        if request.method == 'POST':
            stud = request.form.get('sid')
            sgrades = blockchain.show_grades(stud)
            if len(sgrades["grades"]) == 0:
                return render_template('home/search-grades.html', segment='show_grades')
            return render_template('home/show-grades.html', segment='show_grades', grades = sgrades, lg = len(sgrades["grades"]), bc = blockchain.chain, sid = stud)
        else:
            return render_template('home/search-grades.html', segment='show_grades')
    return render_template('home/page-403.html'), 403

@blueprint.route('/add_grades', methods=['GET', 'POST'])
@login_required
def addg():
    if current_user.role != 99 | 1:
        return render_template('home/page-403.html'), 403
    if request.method == 'POST':
        stud = request.form.get('student').split(',')
        ins = request.form.get('instructor').split(',')
        subj = request.form.get('subject').split(',')
        grade = request.form.get('grade')

        data = {
            "type": "grade",
            "subject": {
                "name": subj[0],
                "id": subj[1]
            },
            "grade": grade,
            "instructor": {
                "name": ins[0],
                "id": ins[1]
            },
            "student": {
                "name": stud[0],
                "id": stud[1]
            }
        }
        #
        grades = blockchain.show_grades(stud[1])
        for x in range(len(grades["grades"])):
            if subj[1] == grades["grades"][x]["subject"]["id"]:
                #print(grades["grades"][x]["subject"]["id"]+" -> Already Graded")
                return render_template('home/add_grades.html', segment = 'add_grades', bc = blockchain.chain, graded = False, lc = len(blockchain.chain), ts = grades["grades"][x]["timestamp"], sname = grades["name"] , subid = grades["grades"][x]["subject"]["id"])
        
        xblock = blockchain.create_block(data)
        return render_template('home/add_grades.html', segment = 'add_grades', bc = blockchain.chain, latestb = xblock, lc = len(blockchain.chain), graded = True, sname = data["student"]["name"])
    else:
        if current_user.role == 99 | 1:
            return render_template('home/add_grades.html', segment = 'add_grades', bc = blockchain.chain, lc = len(blockchain.chain))

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/unused-templates/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
