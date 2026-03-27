from pydantic import BaseModel, Field

class InputClient(BaseModel):
    # Личная информация
    customer_id: str = Field(title='Customer ID', description='A unique ID that identifies each customer')
    gender: str = Field(title='Gender', description="The customer's gender: Male, Female")
    age: int = Field(title='Age', description="The customer's current age, in years, at the time the fiscal quarter ended (Q2 2022)")
    married: str = Field(title='Married', description="Indicates if the customer is married: Yes, No")
    number_of_dependents: int = Field(title='Number of Dependents', description="Indicates the number of dependents that live with the customer")
    city: str = Field(title='City', description="The city of the customer's primary residence in California")
    
    # Геоданные
    zip_code: int = Field(title='Zip Code', description="The zip code of the customer's primary residence")
    latitude: float = Field(title='Latitude', description="The latitude of the customer's primary residence")
    longitude: float = Field(title='Longitude', description="The longitude of the customer's primary residence")
    
    # Поведенческие и договорные данные
    number_of_referrals: int = Field(title='Number of Referrals', description="Indicates the number of times the customer has referred a friend or family member")
    tenure_in_months: int = Field(title='Tenure in Months', description="Total amount of months that the customer has been with the company")
    offer: str = Field(title='Offer', description="The last marketing offer that the customer accepted: None, Offer A, Offer B, Offer C, Offer D, Offer E")
    
    # Услуги телефонии
    phone_service: str = Field(title='Phone Service', description="Indicates if the customer subscribes to home phone service: Yes, No")
    avg_monthly_long_distance_charges: float = Field(title='Avg Monthly Long Distance Charges', description="Customer's average long distance charges")
    multiple_lines: str = Field(title='Multiple Lines', description="Indicates if the customer subscribes to multiple telephone lines: Yes, No")
    
    # Услуги интернета
    internet_service: str = Field(title='Internet Service', description="Indicates if the customer subscribes to Internet service: Yes, No")
    internet_type: str = Field(title='Internet Type', description="Type of internet connection: DSL, Fiber Optic, Cable, None")
    avg_monthly_gb_download: float = Field(title='Avg Monthly GB Download', description="Customer's average download volume in gigabytes")
    online_security: str = Field(title='Online Security', description="Indicates if the customer subscribes to online security service: Yes, No")
    online_backup: str = Field(title='Online Backup', description="Indicates if the customer subscribes to online backup service: Yes, No")
    device_protection_plan: str = Field(title='Device Protection Plan', description="Indicates if the customer subscribes to device protection plan: Yes, No")
    premium_tech_support: str = Field(title='Premium Tech Support', description="Indicates if the customer subscribes to premium tech support: Yes, No")
    streaming_tv: str = Field(title='Streaming TV', description="Indicates if the customer streams television programming: Yes, No")
    streaming_movies: str = Field(title='Streaming Movies', description="Indicates if the customer streams movies: Yes, No")
    streaming_music: str = Field(title='Streaming Music', description="Indicates if the customer streams music: Yes, No")
    unlimited_data: str = Field(title='Unlimited Data', description="Indicates if the customer has unlimited data: Yes, No")
    
    # Счета и финансы
    contract: str = Field(title='Contract', description="Customer's current contract type: Month-to-Month, One Year, Two Year")
    paperless_billing: str = Field(title='Paperless Billing', description="Indicates if the customer has chosen paperless billing: Yes, No")
    payment_method: str = Field(title='Payment Method', description="How the customer pays their bill: Bank Withdrawal, Credit Card, Mailed Check")
    monthly_charge: float = Field(title='Monthly Charge', description="Customer's current total monthly charge for all services")
    total_charges: float = Field(title='Total Charges', description="Customer's total charges, calculated to the end of the quarter")
    total_refunds: float = Field(title='Total Refunds', description="Customer's total refunds, calculated to the end of the quarter")
    total_extra_data_charges: int = Field(title='Total Extra Data Charges', description="Customer's total charges for extra data downloads")
    total_long_distance_charges: float = Field(title='Total Long Distance Charges', description="Customer's total charges for long distance")
    total_revenue: float = Field(title='Total Revenue', description="Company's total revenue from this customer")