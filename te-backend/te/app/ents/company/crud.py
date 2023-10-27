from sqlalchemy.orm import Session

import app.ents.company.models as company_models
import app.ents.company.schema as company_schema
from app.core.config import settings


def read_company_by_name(db: Session, *, name: str) -> company_models.Company | None:
    return (
        db.query(company_models.Company)
        .filter(company_models.Company.name == name)
        .first()
    )


def read_company_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> list[company_models.Company]:
    return db.query(company_models.Company).offset(skip).limit(limit).all()


def create_company(
    db: Session, *, data: company_schema.CompanyCreate
) -> company_models.Company:
    company = company_models.Company(
        **(data.dict(exclude={"location", "referral_materials"}))
    )
    company.image = (settings.CLEAR_BIT_BASE_URL + data.domain) if data.domain else ""
    location = company_models.Location(**data.location.dict())
    company.locations.append(location)

    referral_materials = company_models.ReferralMaterials()
    if data.referral_materials:
        referral_materials = company_models.ReferralMaterials(
            **data.referral_materials.dict()
        )

    company.referral_materials = referral_materials

    db.add(location)
    db.add(referral_materials)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def add_location(
    db: Session,
    *,
    company: company_models.Company,
    data: company_schema.LocationBase,
):
    location = company_models.Location(**data.dict())
    company.locations.append(location)

    db.add(location)
    db.add(company)
    db.commit()
    db.refresh(location)
    db.refresh(company)
    return company


# def update(
#     db: Session,
#     *,
#     db_obj: company_models.Company,
#     data: company_schema.CompanyUpdate | dict[str, Any],
# ) -> company_models.Company:
#     if isinstance(data, dict):
#         update_data = data
#     else:
#         update_data = data.dict(exclude_unset=True)
#     if update_data["password"]:
#         hashed_password = security.get_password_hash(update_data["password"])
#         del update_data["password"]
#         update_data["hashed_password"] = hashed_password
#     return super().update(db, db_obj=db_obj, data=update_data)
