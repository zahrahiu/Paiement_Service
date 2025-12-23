from flask import Flask, request
from flask_restx import Api, Resource, fields
from db import paiements_collection
from DTO.RequestDtoPaiement import RequestDtoPaiement
from Service.PaiementService import PaiementService
from Repository.PaiementRepository import PaiementRepository

app = Flask(__name__)
api = Api(app, title="Paiement API", version="1.0")

ns = api.namespace("paiements", description="Gestion des paiements")

paiement_model = api.model("Paiement", {
    "id": fields.Integer,
    "facture_id": fields.Integer(required=True),
    "montant": fields.Float(required=True),
    "mode": fields.String(required=True),
    "statut": fields.String
})

repo = PaiementRepository(paiements_collection.database)
service = PaiementService(repo)

@ns.route("/")
class PaiementList(Resource):
    @ns.expect(paiement_model)
    @ns.marshal_with(paiement_model)
    def post(self):
        dto = RequestDtoPaiement.from_dict(request.json)
        return service.effectuer_paiement(dto).to_dict()

@ns.route("/<int:id>")
class PaiementResource(Resource):
    @ns.marshal_with(paiement_model)
    def get(self, id):
        paiement = service.get_paiement(id)
        if paiement:
            return paiement.to_dict()
        api.abort(404, "Paiement non trouvé")

if __name__ == "__main__":
    app.run(debug=True, port=8090)
