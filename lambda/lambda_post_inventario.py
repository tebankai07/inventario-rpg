import json
import boto3

from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('InventarioArmas')

def lambda_handler(event, context):
    print("DEBUG EVENT:", json.dumps(event))
    
    try:
        datos = json.loads(event['body'])

        arma = {
            'arma_id': datos['arma_id'],
            'nombre': datos['nombre'],
            'tipo': datos['tipo'],
            'dano': int(datos['dano']),
            'rareza': datos['rareza'],
            'disponible': datos['disponible']
        }

        tabla.put_item(Item=arma)

        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': 'Arma insertada exitosamente'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
