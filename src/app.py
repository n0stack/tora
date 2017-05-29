# coding:UTF-8
import resource.vm as VMres
import resource.info as Infores

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


api.add_resource(VMres.Status, '/vm/status')
api.add_resource(VMres.Create, '/vm/create')
api.add_resource(VMres.Delete, '/vm/delete')

api.add_resource(Infores.DomainAll, '/vm/info')
api.add_resource(Infores.Domain, '/vm/info/<string:name>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
