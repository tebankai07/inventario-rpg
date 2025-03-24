import json
import boto3

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('InventarioArmas')

def lambda_handler(event, context):
    print("DEBUG EVENT:", json.dumps(event))

    try:
        arma_id = event['pathParameters']['id'].strip()
        datos = json.loads(event['body'])

        atributos = {
            'nombre': datos['nombre'],
            'tipo': datos['tipo'],
            'dano': int(datos['dano']),
            'rareza': datos['rareza'],
            'disponible': datos['disponible']
        }

        response = tabla.update_item(
            Key={'arma_id': arma_id},
            UpdateExpression="SET nombre=:n, tipo=:t, dano=:d, rareza=:r, disponible=:dp",
            ExpressionAttributeValues={
                ':n': atributos['nombre'],
                ':t': atributos['tipo'],
                ':d': atributos['dano'],
                ':r': atributos['rareza'],
                ':dp': atributos['disponible']
            },
            ReturnValues="ALL_NEW"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Arma actualizada exitosamente',
                'arma': response['Attributes']
            }, default=str),
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