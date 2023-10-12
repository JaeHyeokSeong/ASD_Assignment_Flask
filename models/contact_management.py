class ContactManagement:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def get_associated_contacts(self, user_id, user_type):
        if user_type == 'agent':
            query = """
                SELECT properties.*, 
                       landlord.name AS landlord_name, landlord.email AS landlord_email, landlord.phone AS landlord_phone,
                       tenant.name AS tenant_name, tenant.email AS tenant_email, tenant.phone AS tenant_phone
                FROM properties
                LEFT JOIN users AS landlord ON properties.landlord_id = landlord.id
                LEFT JOIN users AS tenant ON properties.tenant_id = tenant.id
                WHERE properties.agent_id = %s
                """
        elif user_type == 'landlord':
            query = """
                SELECT properties.*, 
                       agent.name AS agent_name, agent.email AS agent_email, agent.phone AS agent_phone,
                       tenant.name AS tenant_name, tenant.email AS tenant_email, tenant.phone AS tenant_phone
                FROM properties
                LEFT JOIN users AS agent ON properties.agent_id = agent.id
                LEFT JOIN users AS tenant ON properties.tenant_id = tenant.id
                WHERE properties.landlord_id = %s
                """
        elif user_type == 'tenant':
            query = """
                SELECT properties.*, 
                       agent.name AS agent_name, agent.email AS agent_email, agent.phone AS agent_phone,
                       landlord.name AS landlord_name, landlord.email AS landlord_email, landlord.phone AS landlord_phone
                FROM properties
                LEFT JOIN users AS agent ON properties.agent_id = agent.id
                LEFT JOIN users AS landlord ON properties.landlord_id = landlord.id
                WHERE properties.tenant_id = %s
                """
        else:
            return []

        self.mycursor.execute(query, (user_id,))

        # Convert result to a list of dictionaries
        column_names = [desc[0] for desc in self.mycursor.description]
        result = [dict(zip(column_names, row)) for row in self.mycursor.fetchall()]

        return result

    def parse_contacts(self, all_contacts, user_type):
        agents_contacts = []
        landlords_contacts = []
        tenants_contacts = []

        if user_type == 'agent':
            landlords_contacts = [
                {
                    "name": contact["landlord_name"],
                    "property": contact["address"],
                    "email": contact["landlord_email"],
                    "phone_number": contact["landlord_phone"]
                }
                for contact in all_contacts
            ]
            tenants_contacts = [
                {
                    "name": contact["tenant_name"],
                    "property": contact["address"],
                    "email": contact["tenant_email"],
                    "phone_number": contact["tenant_phone"]
                }
                for contact in all_contacts
            ]
        elif user_type == 'landlord':
            agents_contacts = [
                {
                    "name": contact["agent_name"],
                    "property": contact["address"],
                    "email": contact["agent_email"],
                    "phone_number": contact["agent_phone"]
                }
                for contact in all_contacts
            ]
            tenants_contacts = [
                {
                    "name": contact["tenant_name"],
                    "property": contact["address"],
                    "email": contact["tenant_email"],
                    "phone_number": contact["tenant_phone"]
                }
                for contact in all_contacts
            ]
        elif user_type == 'tenant':
            agents_contacts = [
                {
                    "name": contact["agent_name"],
                    "property": contact["address"],
                    "email": contact["agent_email"],
                    "phone_number": contact["agent_phone"]
                }
                for contact in all_contacts
            ]
            landlords_contacts = [
                {
                    "name": contact["landlord_name"],
                    "property": contact["address"],
                    "email": contact["landlord_email"],
                    "phone_number": contact["landlord_phone"]
                }
                for contact in all_contacts
            ]

        return agents_contacts, landlords_contacts, tenants_contacts