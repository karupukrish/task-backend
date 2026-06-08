"""Seed script to populate the database with initial data.

Usage:
    python seed.py

Requirements:
    - PostgreSQL must be running and accessible via DATABASE_URL (env var or .env file)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Base
from app.models import Admin, Developer, Project, Task, ProjectStatus, TaskStatus
from app.auth import hash_password


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # ── Admin ──
        existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
        if not existing_admin:
            admin = Admin(username="admin", password_hash=hash_password("admin123"))
            db.add(admin)
            print("✓ Created admin user (username: admin, password: admin123)")
        else:
            print("→ Admin already exists, skipping")

        # ── Developers ──
        devs_data = [
            ("Alice Johnson", "alice@example.com", "pass123"),
            ("Bob Smith", "bob@example.com", "pass123"),
            ("Carol Davis", "carol@example.com", "pass123"),
        ]
        created_devs = []
        for name, email, pw in devs_data:
            existing = db.query(Developer).filter(Developer.email == email).first()
            if not existing:
                dev = Developer(name=name, email=email, password_hash=hash_password(pw))
                db.add(dev)
                db.flush()
                created_devs.append(dev)
                print(f"✓ Created developer: {name} ({email})")
            else:
                created_devs.append(existing)
                print(f"→ Developer {email} already exists, skipping")

        # ── Projects ──
        projs_data = [
            ("E-Commerce Platform", "Build a full-featured online store with payment integration", ProjectStatus.IN_PROGRESS),
            ("Mobile Chat App", "Real-time messaging app for iOS and Android", ProjectStatus.PLANNING),
            ("Internal Dashboard", "Admin dashboard for monitoring company metrics", ProjectStatus.COMPLETED),
        ]
        created_projs = []
        for name, desc, status in projs_data:
            existing = db.query(Project).filter(Project.name == name).first()
            if not existing:
                proj = Project(name=name, description=desc, status=status)
                db.add(proj)
                db.flush()
                created_projs.append(proj)
                print(f"✓ Created project: {name}")
            else:
                created_projs.append(existing)
                print(f"→ Project '{name}' already exists, skipping")

        # ── Tasks ──
        if created_devs and created_projs:
            tasks_data = [
                ("Set up payment gateway", "Integrate Stripe for payment processing", TaskStatus.IN_PROGRESS, created_projs[0], created_devs[0]),
                ("Design product catalog", "Create product listing and search functionality", TaskStatus.PENDING, created_projs[0], created_devs[1]),
                ("Implement WebSocket chat", "Set up real-time messaging using WebSockets", TaskStatus.PENDING, created_projs[1], created_devs[0]),
                ("User authentication module", "Build login/register with JWT", TaskStatus.PENDING, created_projs[1], created_devs[2]),
                ("Create revenue charts", "Add chart.js visualizations for revenue data", TaskStatus.COMPLETED, created_projs[2], created_devs[1]),
                ("Build user management page", "CRUD interface for managing users", TaskStatus.IN_PROGRESS, created_projs[2], created_devs[2]),
            ]
            for title, desc, status, proj, dev in tasks_data:
                existing = db.query(Task).filter(Task.title == title, Task.project_id == proj.id).first()
                if not existing:
                    task = Task(title=title, description=desc, status=status, project_id=proj.id, developer_id=dev.id)
                    db.add(task)
                    print(f"✓ Created task: '{title}' → project: '{proj.name}', developer: '{dev.name}'")
                else:
                    print(f"→ Task '{title}' already exists, skipping")

        db.commit()
        print("\n✅ Seeding complete!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
