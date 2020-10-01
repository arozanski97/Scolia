from flask import Flask, redirect, url_for, render_template,Blueprint,request, jsonify
from flask_mail import Mail, Message,current_app

mod=Blueprint('frontend',__name__,template_folder='templates',static_folder='static',static_url_path='/frontend/static')
from webserver import mail
from webserver.backend import routes as backend_mod
app = Flask(__name__)


@mod.route("/")
def homepage():
    return render_template("index.html")

@mod.route("/genomeassembly")
def genomeassembly():
    return render_template("GenomeAssembly.html")

@mod.route("/geneprediction")
def geneprediction():
    return render_template("GenePrediction.html")

@mod.route("/func-ann")
def functionalannotation():
    return render_template("FunctionalAnnotation.html")

@mod.route("/comp-gen")
def comparativegenomics():
    return render_template("ComparativeGenomics.html")

@mod.route("/AboutUs")
def aboutus():
    return render_template("AboutUs.html")

@mod.route("/submit")
def submit():
    return render_template("submit.html")

@mod.route('/Genome_Assembly',methods=['POST'])
def Genome_Assembly():
	Tools=[]
	email=request.form.get("assem_email")
	needs_trimming=request.form.get("needs_trimming")
	if needs_trimming=='on':
		Tools=Tools+['trim']
	spades=request.form.get("spades")
	if spades == 'on':
		Tools=Tools+['spades']
	skesa=request.form.get("skesa")
	if skesa == 'on':
		Tools=Tools+['skesa']
	if ('file1' not in request.files):
		resp=jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file1 = request.files['file1']
	files=[file1]
	did_send=backend_mod.backend_setup(files,email,1,Tools)
	if did_send:
		confirm_msg='File Submitted!'
		return render_template("submit.html",confirm_msg=confirm_msg)
@mod.route('/Gene_Prediction',methods=['POST'])
def Gene_Prediction():
	Tools=[]
	email=request.form.get('gen_email')
	if ('file1' not in request.files) or ('file2' not in request.files):
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file1 = request.files['file1']
	file2 = request.files['file2']
	files=[file1,file2]
	did_send=backend_mod.backend_setup(files,email,2,Tools)
	if did_send:
		confirm_msg='File Submitted!'
		return render_template("submit.html",confirm_msg=confirm_msg)
@mod.route('/Functional_Annotation',methods=['POST'])
def Functional_Annotation():
	Tools=[]
	email=request.form.get("ann_email")
	card_rgi=request.form.get("card_rgi")
	if card_rgi == 'on':
		Tools=Tools+['card_rgi']
	vfdb=request.form.get("vfdb")
	if vfdb == 'on':
		Tools=Tools+['vfdb']
	eggnog=request.form.get("eggnog")
	if eggnog == 'on':
		Tools=Tools+['eggnog']
	pilercr=request.form.get("pilercr")
	if pilercr == 'on':
		Tools=Tools+['pilercr']
	#print(email)
	# check if the post request has the file part
	if ('file1' not in request.files):
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file1 = request.files['file1']
	files=[file1]
	did_send=backend_mod.backend_setup(files,email,3,Tools)
	if did_send:
		confirm_msg='File Submitted!'
		return render_template("submit.html",confirm_msg=confirm_msg)
@mod.route('/Comparative_Genomics',methods=['POST'])
def Comparative_Genomics():
	Tools=[]
	email=request.form.get("comp_email")
	fast_ani=request.form.get("fast_ani")
	if fast_ani == 'on':
		Tools=Tools+['fast_ani']
	string_mlst=request.form.get("string_mlst")
	if string_mlst == 'on':
		Tools=Tools+['string_mlst']
	ksnp=request.form.get("ksnp")
	if ksnp == 'on':
		Tools=Tools+['ksnp']
	#print(ksnp)
	#print(Tools)
	if ('file1' not in request.files):
                resp = jsonify({'message' : 'No file part in the request'})
                resp.status_code = 400
                return resp
	file1 = request.files['file1']
	file2 = request.files['file2']
	if file2.filename =='':
		files=[file1]
	else:
		files=[file1,file2]
	did_send=backend_mod.backend_setup(files,email,4,Tools)
	if did_send:
		confirm_msg='File Submitted!'
		return render_template("submit.html",confirm_msg=confirm_msg)
