# ER-диаграмма: Агентство недвижимости (вариант 26)

```mermaid
erDiagram
    User ||--|| Employee : "OneToOne"
    PropertyType ||--o{ RealEstate : "FK primary"
    PropertyType }o--o{ RealEstate : "M2M additional"
    Owner ||--o{ RealEstate : "FK"
    RealEstate ||--o{ Deal : "FK"
    Employee ||--o{ Deal : "FK"
    Buyer ||--o{ Deal : "FK"

    PropertyType {
        int id PK
        string name
        text description
    }

    Owner {
        int id PK
        string full_name
        string phone
        string email
        datetime created_at
    }

    RealEstate {
        int id PK
        string code UK
        string title
        string address
        decimal area
        decimal price
        int rooms
        int floor
        text description
        image photo
        string status
        datetime created_at
        datetime updated_at
    }

    Employee {
        int id PK
        int user_id FK
        string department
        string position
        string phone
        date birth_date
        image photo
        date hired_date
    }

    Buyer {
        int id PK
        string full_name
        string phone
        string email
        date birth_date
        datetime created_at
    }

    Deal {
        int id PK
        string deal_type
        date deal_date
        decimal amount
        datetime created_at
    }

    Article {
        int id PK
        string title
        text content
        string short_content
        image image
        datetime published_at
        bool is_published
    }

    CompanyInfo {
        int id PK
        string section
        string title
        text content
        datetime updated_at
    }

    GlossaryTerm {
        int id PK
        string term
        text definition
        datetime created_at
    }

    Vacancy {
        int id PK
        string title
        text description
        string salary
        bool is_active
    }

    Review {
        int id PK
        string name
        int rating
        text text
        datetime created_at
        bool is_published
    }

    PromoCode {
        int id PK
        string code UK
        decimal discount
        text description
        date valid_from
        date valid_until
        bool is_active
    }
```

## Типы связей

| Связь | Тип | Описание |
|-------|-----|----------|
| User <-> Employee | OneToOne | Профиль сотрудника |
| PropertyType -> RealEstate | ForeignKey | Основной тип объекта |
| PropertyType <-> RealEstate | ManyToMany | Дополнительные типы |
| Owner -> RealEstate | ForeignKey | Владелец объекта |
| RealEstate -> Deal | ForeignKey | Объект сделки |
| Employee -> Deal | ForeignKey | Оформивший сотрудник |
| Buyer -> Deal | ForeignKey | Покупатель/арендатор |
