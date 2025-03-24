import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('InventarioArmas')

def lambda_handler(event, context):
    print("DEBUG EVENT:", json.dumps(event))

    try:
        arma_id = event['pathParameters']['id'].strip()

        respuesta = tabla.get_item(Key={'arma_id': arma_id})

        if 'Item' not in respuesta:
            return {
                'statusCode': 404,
                'body': json.dumps({'mensaje': 'Arma no encontrada'}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        # Convertir los datos decimales a string para que sean serializables
        item = respuesta['Item']
        for key, value in item.items():
            if isinstance(value, Decimal):
                item[key] = int(value)

        return {
            'statusCode': 200,
            'body': json.dumps(item),
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