from sqlalchemy.orm import Session
import models


def seed_data(db: Session):
    """
    Populates the database with initial review data if it's empty.
    """
    # Check if data already exists to avoid duplicates
    if db.query(models.Review).count() > 0:
        print("⚠️  Database already contains data. Skipping seed.")
        return

    print("🌱 Seeding Review Data...")

    reviews = [
        # Smartphone (ID 1)
        models.Review(product_id=1, user_name='TechReviewer',
                      rating=5, comment='Great battery life, lasts 2 days!'),
        models.Review(product_id=1, user_name='Alice Dev', rating=4,
                      comment='Good, but a bit expensive for the specs.'),
        models.Review(product_id=1, user_name='PhotoPro', rating=5,
                      comment='The AI camera night mode is insane.'),

        # Laptop (ID 2)
        models.Review(product_id=2, user_name='DevDave', rating=5,
                      comment='Compiles my monolithic Java app in seconds!'),
        models.Review(product_id=2, user_name='MobileWarrior', rating=3,
                      comment='Battery life is average when running Docker containers.'),

        # Microservices Book (ID 3)
        models.Review(product_id=3, user_name='Bob Ops', rating=5,
                      comment='Changed my career. A must-read.'),
        models.Review(product_id=3, user_name='Student101', rating=4,
                      comment='Concepts are great, but examples are dense.'),

        # Headphones (ID 4)
        models.Review(product_id=4, user_name='Audiophile', rating=3,
                      comment='Bass is too heavy for classical music.'),
        models.Review(product_id=4, user_name='Commuter', rating=5,
                      comment='Noise cancellation is a lifesaver on the train.'),

        # Keyboard (ID 5)
        models.Review(product_id=5, user_name='GamerOne', rating=5,
                      comment='Clicky keys are satisfying. RGB is bright.'),
        models.Review(product_id=5, user_name='OfficeWorker', rating=2,
                      comment='Too loud for the office, coworkers hate me.'),

        # Monitor (ID 6)
        models.Review(product_id=6, user_name='PixelPeepers', rating=4,
                      comment='Colors are accurate, but the stand is a bit wobbly.'),
        models.Review(product_id=6, user_name='DualScreenGuy', rating=5,
                      comment='Bought two of these. Productivity skyrocketed.'),

        # Clean Code Book (ID 7)
        models.Review(product_id=7, user_name='JuniorDev', rating=5,
                      comment='Every developer must read this at least once.'),

        # Mouse (ID 8)
        models.Review(product_id=8, user_name='CarpalTunnelSurvivor',
                      rating=5, comment='My wrist pain vanished after two days.'),
        models.Review(product_id=8, user_name='ClickyFan', rating=4,
                      comment='Takes some getting used to, but very comfortable.')
    ]

    try:
        db.add_all(reviews)
        db.commit()
        print(f"✅ Successfully seeded {len(reviews)} reviews!")
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
