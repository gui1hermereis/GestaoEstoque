from tagoio_sdk import Resources

# Configurações
access_token = "477d0200-d3b5-4302-9b4d-1b4b5f7d5638"
device_id = "680c19c90f970e000ae86d3f"

resources = Resources({"token": access_token})

# ------------------ EXCLUSÃO DE DADOS ------------------
def delete_all_device_data(device_id):
    try:
        batch_size = 15  
        while True:
            data = resources.devices.getDeviceData(device_id, {"page": 1, "per_page": batch_size})
            
            if not data:  
                print(f"Todos os dados foram excluídos com sucesso para o dispositivo {device_id}.")
                return True 
            
            record_ids = [record['id'] for record in data]
            
            response = resources.devices.deleteDeviceData(device_id, {"ids": record_ids})
            
            if isinstance(response, str) and "Data Removed" in response:
                print(f"Resposta da API: {response}")
            else:
                print(f"Falha ao excluir dados: {response}")
                return False 

    except Exception as e:
        print(f"Erro ao excluir dados: {e}")
        return False 
    
# ------------------ MAIN ------------------
def main():
    delete_all_device_data(device_id)

if __name__ == "__main__":
    main()