from flask import Flask, render_template, url_for, request, redirect, json
from SPARQLWrapper import SPARQLWrapper, JSON
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from flask import Flask, render_template, json, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', tasks=[])

@app.route('/Stores', methods=['GET','POST'])
def detail():
    if request.method == 'GET':
        p = request.args.get('id')
        print(p)
        sparql = SPARQLWrapper("http://18.218.190.18:3030/db1/sparql")
        sparql.setQuery(
            """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX loc:	<http://www.semanticweb.org/tarunsnehithkishorereddykarna/ontologies/2020/10/untitled-ontology-16#>
        PREFIX use:	<http://www.semanticweb.org/anushakolan/ontologies/2020/10/untitled-ontology-14#>
        PREFIX det: <http://www.semanticweb.org/tarunsnehithkishorereddykarna/ontologies/2020/10/untitled-ontology-15#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT  ?name ?rating ?street ?city ?state ?postal ?open ?cate
        WHERE {
        SERVICE <http://18.216.61.64:3030/db1/query>
                {
        SELECT ?store ?elat ?elong ?id 
        WHERE {
                        SERVICE <http://18.222.233.173:3030/db1/sparql>
                        {
                        SELECT  ?name  ?lat ?lon 
                    WHERE {
                        
                            ?name rdf:type use:User;
                                use:has_screen_name '%s';
                                use:has_latitude ?lat;
                                use:has_longitude ?lon.
                        }
        }
            ?store rdf:type loc:Store.
            ?store loc:has_BusinessID ?id.
            ?store loc:has_Location ?loc.
            ?loc loc:has_Latitude ?elat.
            ?loc loc:has_Longitude ?elong.
            FILTER((abs(xsd:float(?lat) - xsd:float(?elat)) < 5) && (abs(xsd:float(?lon) - xsd:float(?elong)) < 5))
        }
        ORDER BY ((abs(xsd:float(?lat) - xsd:float(?elat))) && (abs(xsd:float(?lon) - xsd:float(?elong))))
            LIMIT 100
        }
        ?st rdf:type det:Store.
        ?st det:has_Business_ID ?id.
        ?st det:has_name ?name.
        ?st det:has_Rating ?rating.
        ?st det:has_Address ?ad.
        ?ad det:has_City ?city.
        ?ad det:has_State ?state.
        ?ad det:has_StreetNo ?street.
        ?ad det:has_PostalCode ?postal.
        ?st det:has_IsOpen ?open.
        ?st det:has_Catogories ?cate.
        
        }
        #ORDER BY DESC (xsd:float(?rating))
        LIMIT 20""" % (p))
        sparql.setReturnFormat(JSON)
        data=sparql.query().convert()
        cols = data["head"]["vars"]
        rows = data["results"]["bindings"]
        s=set()
        users = []
        stat = " "
    
        for i in range(len(rows)):
            
        
            if rows[i][cols[6]]['value'] == "0":
                stat = "CLOSED"
            else:
                stat = "OPEN"
            users.append({ "name": rows[i][cols[0]]['value'],"rating": rows[i][cols[1]]['value'],"street": rows[i][cols[2]]['value'],"city": rows[i][cols[3]]['value']
            ,"state": rows[i][cols[4]]['value'],"postal": rows[i][cols[5]]['value'],"Open": stat,"cate": rows[i][cols[7]]['value']})
            che = rows[i][cols[7]]['value'].split(",")
            for ch in che:
                s.add(ch.strip()) 
        users.append({"id":p})
        users.append({"categories":s})  
        return render_template('stores.html', tasks= users )




    if request.method == 'POST':
        p = request.form['categories']
        k = p.split('&')
   
        sparql = SPARQLWrapper("http://18.218.190.18:3030/db1/sparql")
        sparql.setQuery(
            """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX loc:	<http://www.semanticweb.org/tarunsnehithkishorereddykarna/ontologies/2020/10/untitled-ontology-16#>
        PREFIX use:	<http://www.semanticweb.org/anushakolan/ontologies/2020/10/untitled-ontology-14#>
        PREFIX det: <http://www.semanticweb.org/tarunsnehithkishorereddykarna/ontologies/2020/10/untitled-ontology-15#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT  ?name ?rating ?street ?city ?state ?postal ?open ?cate
        WHERE {
        SERVICE <http://18.216.61.64:3030/db1/query>
                {
        SELECT ?store ?elat ?elong ?id 
        WHERE {
                        SERVICE <http://18.222.233.173:3030/db1/sparql>
                        {
                        SELECT  ?name  ?lat ?lon 
                    WHERE {
                        
                            ?name rdf:type use:User;
                                use:has_screen_name '%s';
                                use:has_latitude ?lat;
                                use:has_longitude ?lon.
                        }
        }
            ?store rdf:type loc:Store.
            ?store loc:has_BusinessID ?id.
            ?store loc:has_Location ?loc.
            ?loc loc:has_Latitude ?elat.
            ?loc loc:has_Longitude ?elong.
            FILTER((abs(xsd:float(?lat) - xsd:float(?elat)) < 5) && (abs(xsd:float(?lon) - xsd:float(?elong)) < 5))
        }
        ORDER BY ((abs(xsd:float(?lat) - xsd:float(?elat))) && (abs(xsd:float(?lon) - xsd:float(?elong))))
            LIMIT 100
        }
        ?st rdf:type det:Store.
        ?st det:has_Business_ID ?id.
        ?st det:has_name ?name.
        ?st det:has_Rating ?rating.
        ?st det:has_Address ?ad.
        ?ad det:has_City ?city.
        ?ad det:has_State ?state.
        ?ad det:has_StreetNo ?street.
        ?ad det:has_PostalCode ?postal.
        ?st det:has_IsOpen ?open.
        ?st det:has_Catogories ?cate.
        }
        #ORDER BY DESC (xsd:float(?rating))
        LIMIT 20""" % (k[1]))
        sparql.setReturnFormat(JSON)
        data=sparql.query().convert()
        cols = data["head"]["vars"]
        rows = data["results"]["bindings"]
        s=set()
        users = []
        stat = " "
    
        for i in range(len(rows)):
            
            if k[0] not in rows[i][cols[7]]['value']:
                continue
            if rows[i][cols[6]]['value'] == "0":
                stat = "CLOSED"
            else:
                stat = "OPEN"
            users.append({ "name": rows[i][cols[0]]['value'],"rating": rows[i][cols[1]]['value'],"street": rows[i][cols[2]]['value'],"city": rows[i][cols[3]]['value']
            ,"state": rows[i][cols[4]]['value'],"postal": rows[i][cols[5]]['value'],"Open": stat,"cate": rows[i][cols[7]]['value']})
            che = rows[i][cols[7]]['value'].split(",")
            for ch in che:
                s.add(ch.strip()) 
        users.append({"id":k[1]})
        users.append({"categories":s})
        return render_template('stores.html', tasks= users)


    
@app.route('/findusers', methods=['Post'])
def search():
    user=request.form["keyword"].strip()
  
    sparql = SPARQLWrapper("http://18.222.233.173:3030/db1/sparql")
    sparql.setQuery(
        """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX loc:	<http://www.semanticweb.org/tarunsnehithkishorereddykarna/ontologies/2020/10/untitled-ontology-16#>
        PREFIX use:	<http://www.semanticweb.org/anushakolan/ontologies/2020/10/untitled-ontology-14#>
        PREFIX det: <http://www.semanticweb.org/tarunsnehithkishorereddykarna/ontologies/2020/10/untitled-ontology-15#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?id ?name 
        WHERE {
	        ?person rdf:type use:User;
         	use:has_user_name ?name;
            use:has_screen_name ?id.
             FILTER( regex(?name, '%s', "i" ) ) 

             }LIMIT 100""" % (user))
    sparql.setReturnFormat(JSON)
    data=sparql.query().convert()
   
    cols = data["head"]["vars"]
    rows = data["results"]["bindings"]
    users = []
    for i in range(len(rows)):
        
        users.append({"id": rows[i][cols[0]]['value'], "name": rows[i][cols[1]]['value']})
    
    return render_template('index.html', tasks=users)

@app.route('/recommend', methods=['Post'])
def recommendations():
    events = '[{"id":"11", "name" : "sun burn"}, {"id":"12" ,"name" : "kochela"},{"id":"13" , "name": "sreemantam"}]'
    tasks = json.loads(events)
    return render_template('events.html', tasks=tasks)
# pip
# @app.route('/hotels', methods=['GET'])
# def hotel():
#     hotels = '[{"id":"21", "name" : "novotel"}, {"id":"22" ,"name" : "marriot"},{"id":"23" , "name": "taj"}]'
#     tasks = json.loads(hotels)
#     return render_template('hotels.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)