```
app/
│
├── main.py                        # FastAPI application entry point
├── config.py                      # Application settings
│
├── core/
│   ├── auth.py
│   ├── security.py
│   ├── exceptions.py
│   ├── middleware.py
│   ├── permissions.py
│   └── dependencies.py
│
├── database/
│   ├── base.py                    # BaseModel, AuditModel
│   ├── session.py                 # AsyncSession
│   ├── engine.py
│   └── seed.py
│
├── common/
│   ├── pagination.py
│   ├── responses.py
│   ├── validators.py
│   ├── enums.py
│   ├── constants.py
│   └── utils.py
│
├── modules/
│
│   ├── location/
│   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Includes all location routes
│   │   │   ├── country.py
│   │   │   ├── state.py
│   │   │   ├── district.py
│   │   │   ├── city.py
│   │   │   └── branch.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── country.py
│   │   │   ├── state.py
│   │   │   ├── district.py
│   │   │   ├── city.py
│   │   │   └── branch.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── country.py
│   │   │   ├── state.py
│   │   │   ├── district.py
│   │   │   ├── city.py
│   │   │   └── branch.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── country.py
│   │   │   ├── state.py
│   │   │   ├── district.py
│   │   │   ├── city.py
│   │   │   └── branch.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── country.py
│   │   │   ├── state.py
│   │   │   ├── district.py
│   │   │   ├── city.py
│   │   │   └── branch.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── inventory/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── __init__.py
│   │
│   ├── sales/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── __init__.py
│   │
│   ├── purchase/
│   ├── accounts/
│   ├── hr/
│   ├── crm/
│   ├── reports/
│   └── auth/
│
└── migrations/
    ├── env.py
    ├── script.py.mako
    └── versions/
```