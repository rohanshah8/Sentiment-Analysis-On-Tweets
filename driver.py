import modules
import trending
from flask import Flask,render_template,url_for,request

keys=['Enter keyword','Enter keyword']
kiy=['Enter keyword','Enter keyword']
x1=0
x2=0

app=Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/search')
def search():
	return render_template('search.html',val=keys[0])

@app.route('/saction',methods=['GET','POST'])
def saction():
	kiy=[]
	if request.method == 'GET':
		kiy.insert(0,request.args.get('keyword'))
		x1=modules.do_work(kiy[0])
		#return keys[0]
		return render_template('search.html',key='/static/img/'+kiy[0]+'-bar.png',val=kiy[0])
	else:
		return 'Invalid request'

@app.route('/caction',methods=['GET','POST'])
def caction():
	keys=[]
	if request.method == 'GET':
		if 'keyword1' in request.args:
			keys.insert(0,request.args.get('keyword1'))
			keys.insert(1,request.args.get('keyword2'))

			place = request.args.get('city')
			if place=='delhi':
				x1=modules.do_work_delhi(keys[0])
				x2=modules.do_work_delhi(keys[1])
				keys[1]="".join([keys[1],"-delhi"])
				place="-delhi"
				#keys[0]="".join([keys[0],"-delhi"])
				temp=[keys[0],keys[1]]
				modules.pie_plot(temp,x1,x2)
			elif place=='gujarat':
				x1=modules.do_work_gujarat(keys[0])
				x2=modules.do_work_gujarat(keys[1])
				keys[1]="".join([keys[1],"-gujarat"])
				place="-gujarat"
				#keys[0]="".join([keys[0],"-gujarat"])
				temp=[keys[0],keys[1]]
				modules.pie_plot(temp,x1,x2)
			else :
				x1=modules.do_work(keys[0])
				x2=modules.do_work(keys[1])
				temp=keys
				place=''
				modules.pie_plot(temp,x1,x2)

			temp='pie-chart'+'-'+keys[0]+'-'+keys[1]	
			key1='/static/img/'+keys[0]+place+'-bar.png'
			key2='/static/img/'+keys[1]+'-bar.png'
			key3='/static/img/'+temp+'.png'
			return render_template('compare.html',key1=key1,key2=key2,key3=key3,val=keys,place=place)
		else:
			return 'Wrong'
	else:
		return 'Invalid request'

@app.route('/compare')
def compare():
	return render_template('compare.html',key1='',key2='',key3='',val=keys)

@app.route('/trending')
def trending():
	#trending.find_trending()
	return render_template('trending.html')

	
if __name__ == "__main__" :
    app.run(debug=True)




#x1=modules.do_work("DELL")
#x2=modules.do_work("ASUS")
#modules.pie_plot(['DELL','ASUS'],x1,x2)