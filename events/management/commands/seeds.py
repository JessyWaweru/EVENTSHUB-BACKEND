from email.mime import image

from django.core.management.base import BaseCommand
from datetime import timezone
import random
from faker import Faker
from events.models import User, Sponsor, Event, Speaker, Attendee

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database with 30 events...')
        
        fake = Faker()

        # Delete existing data to start fresh
        Attendee.objects.all().delete()
        Speaker.objects.all().delete()
        Event.objects.all().delete()
        Sponsor.objects.all().delete()
        User.objects.all().delete()

        # Create main user
        user = User.objects.create_user(
            username="user",
            email="user@mail.com",
            password="password",
            gender="Female",
            age=18
        )

        # Create sponsors
        sponsor1 = Sponsor.objects.create(title="Google", organisation="Google Inc.", category="Technology", industry="Software")
        sponsor2 = Sponsor.objects.create(title="Nike", organisation="Nike Inc.", category="Fashion", industry="Sportswear")
        sponsor3 = Sponsor.objects.create(title="Coca-Cola", organisation="The Coca-Cola Company", category="Food and Beverage", industry="Beverages")
        
        sponsors_list = [sponsor1, sponsor2, sponsor3]

        # 1. Your 3 core specific events
        events_data = [
            {
                "price": 1200,
                "event_planner_name": 'Jessica Pear',
                "event_planner_contact": '0703263352',
                "title": "Autism foundation",
                "image": "https://w0.peakpx.com/wallpaper/608/924/HD-wallpaper-autism-speaks-awareness-purple-april-puzzle-asd-autism.jpg",
                "description": "We take a look at how we have come in our knowledge and understanding of Autism",
                "location": "Sabaki Hall, Mombasa",
                "age_limit": "12+",
                "capacity": 500, 
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 2000, 
                "event_planner_name": 'Jess Pear',
                "event_planner_contact": '0777263352',
                "title": "Music Festival",
                "image": "https://images.pexels.com/photos/2263436/pexels-photo-2263436.jpeg",
                "description": "Join us for a day of music, food, and fun!",
                "location": "Vasha Resort",
                "age_limit": "22+",
                "capacity": 5000, 
                "date": fake.date_time_between(start_date='now', end_date='+5d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 1000, 
                "event_planner_name": 'Jessica Pear', 
                "event_planner_contact": '0703263352', 
                "title": "Charity Walk", 
                "image": "https://images.unsplash.com/photo-1699627392109-e39ec21ba078?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "description": "Join us for a charity walk to raise funds for cancer research.", 
                "location": "From Nairobi CBD till Kitengela via the expressway",
                "age_limit": "15+",
                "capacity": 5000, 
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price":2500,
                "event_planner_name":"Captain Mann",
                "event_planner_contact":"0703263326",
                "title":"Jude's birthday party",
                "image": "https://media.istockphoto.com/id/2191575922/photo/multiethnic-friends-company-in-carnival-wear-blowing-in-party-pipes-having-fun.jpg?s=612x612&w=0&k=20&c=bZgLVmiL7J9tg-tmVV72oECHi1d6gpSFZMn8whalzwI=",
                "description": "It is that time of the year.We are back.Jude the influencer is hosting an exclusive party at his beach house in Diani.All are welcomed .At a price.",
                "location": "Diani",
                "age_limit": "21+",
                "capacity": 1000,
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
             },
             {
                "price":3000,
                "event_planner_name":'Henry Danger',
                "event_planner_contact":"0700261126",
                "title":"Fast Festival",
                "image":"data:image/jpeg;base64,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",
                "description": "Join the fast family as the new trailer for their new movie Fast X drops.",
                "location": "Garden City Mall Cinemas",
                "age_limit": "15+",
                "capacity": 200,
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
             }, 
             {
                "price": 500, 
                "event_planner_name": 'Stephon Wardell', 
                "event_planner_contact": '0703251123',
                "title": "Tech Conference", 
                "image": "https://www.tycoonstory.com/wp-content/uploads/2022/09/8-Technology-Trends-That-Will-Change-The-Way-You-Do-Business-Tycoonstory-1.jpg",
                "description": "Join us for a conference on the latest trends in technology.",
                "location": "Sarit Center", 
                "age_limit": "15+", 
                "capacity": 100,
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
             },
             {
                 "price": 1200, 
        "event_planner_name": 'Lebron Jamey', 
        "event_planner_contact": '0703267726',
        "title": "Women CEOs Forum", 
        "image": "https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F470577949%2F180703518709%2F1%2Foriginal.20230316-134707?w=940&auto=format%2Ccompress&q=75&sharp=10&rect=0%2C74%2C1200%2C600&s=f39254b1b6c375d4ac066fbb6e092c73",
        "description": "The Women CEOs Forum is a convention of like-minded women entrepreneurs, enterprise leaders and support organizations from various industries across Africa. The participants will come together to discuss their ambitions, goals, and challenges in the business environment.",
        "location": "Sarit Center", 
        "age_limit": "18+", 
        "capacity": 510,
             }, 
        ]

        # Lists for generating realistic random events
        kenyan_locations = ["Nairobi CBD", "Westlands", "Naivasha", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Kilimani", "Thika", "Diani"]
        event_titles = [
            "Tech Innovators Summit", "Afrobeat Concert", "Startup Pitch Night", "Street Food Festival",
            "Art & Wine Gala", "Marathon Prep Run", "Cultural Tamasha", "Business Networking Brunch",
            "Future of AI Conference", "Gourmet Food Fair", "Digital Marketing Workshop", "Jazz & Blues Night",
            "Global Tech Expo", "Culinary Masterclass", "Professional Networking Mixer", "Indie Music Showcase",
            "Cybersecurity Forum", "Food Truck Fiesta", "Blockchain & Crypto Summit", "Live Comedy Show",
            "Women in Tech Conference", "Sustainable Food Systems Dialogue", "Fintech Innovation Day",
            "Electronic Dance Festival", "Data Science Symposium", "Craft Beer & Bites Festival",
            "Leadership Development Conference"
        ]
       
        images = [
            "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80",# Conference
            "https://plus.unsplash.com/premium_photo-1679547202671-f9dbbf466db4?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y29uZmVyZW5jZXxlbnwwfHwwfHx8MA%3D%3D",
            "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fGNvbmZlcmVuY2V8ZW58MHx8MHx8fDA%3D",
            "https://images.unsplash.com/photo-1594122230689-45899d9e6f69?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGNvbmZlcmVuY2V8ZW58MHx8MHx8fDA%3D",
            "https://media.istockphoto.com/id/2223522049/photo/african-businessman-speaking-at-a-global-economic-strategies-at-international-business.jpg?s=612x612&w=0&k=20&c=EiQxQCPoa6oTipHxoqiB2G8XJHr0Zo3K2V09For86rc=",
            "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=800&q=80", # Concert
            "https://media.istockphoto.com/id/1195008601/photo/this-is-how-you-enter-a-new-year.jpg?s=612x612&w=0&k=20&c=Y9Qwc9EBuTusvlXYZGK4cg-mFAnGhT1FAcN2b-qqNYY=",
            "https://media.istockphoto.com/id/1179757485/photo/the-partys-ours-to-enjoy.jpg?s=612x612&w=0&k=20&c=qlg7opvvB5ZDt5h2YAA1O36_4OA0Y3dARE7hQmwf0HA=",
            "https://media.istockphoto.com/id/1475485430/photo/black-woman-wow-or-dancing-on-dance-floor-in-party-nightclub-event-or-bokeh-disco-for.jpg?s=612x612&w=0&k=20&c=OvebfcGqjqMcymUafmnGzVlfXlDxtoIW7m3LQgvMRB8=",
            "https://media.istockphoto.com/id/2192509787/photo/microphones-seen-on-stage-with-bright-coloful-light.jpg?s=612x612&w=0&k=20&c=yn5W7mDet-9mt8WV7nf7ovQnHEVqd7g63XR5m9BBXmA=",
            "https://images.unsplash.com/photo-1511556532299-8f662fc26c06?w=800&q=80", # Networking
            "https://media.istockphoto.com/id/1064982786/photo/global-communication-network-concept.jpg?s=612x612&w=0&k=20&c=aHRvgchinw71cLE5YBSURjbdOB4zWiOaCIZHg904bek=",
            "https://media.istockphoto.com/id/1393828973/photo/african-map-in-a-digital-raster-micro-structure.jpg?s=612x612&w=0&k=20&c=7fGw5dqqe5vIcnmGHBEJ8eRlMCp0-oY0MSeXk4guv2U=",
            "https://media.istockphoto.com/id/1004007018/photo/green-global-social-network-background.jpg?s=612x612&w=0&k=20&c=enJK2aJPXRFn6UPdvAwxoy-FURiaxTD_v3u_8E9m93o=",
            "https://media.istockphoto.com/id/1199216653/photo/all-african-casual-business-meeting-candid-real-happy-moment-between-four-work-colleagues.jpg?s=612x612&w=0&k=20&c=FHzQ_9LX9GpEuanjFwHI3eNMN1OMHbx9QREEVJuABwY=",
            "https://images.unsplash.com/photo-1555244162-803834f70033?w=800&q=80", # Food
            "https://media.istockphoto.com/id/2222853662/photo/dining-table-on-christmas-or-thanksgiving.jpg?s=612x612&w=0&k=20&c=XvKKsnJguiS-fUVPU-sf9xC885ohbiUXgFImqEmkfz8=",
            "https://media.istockphoto.com/id/2201499922/photo/rose-wine-dinner.jpg?s=612x612&w=0&k=20&c=IbVbzWPgWgh7rvmwpRpemQ-XvJYPaoc1Jpf7zQln3W0=",
            "https://media.istockphoto.com/id/2206546844/photo/young-woman-with-curly-hair-eating-a-slice-of-tangerine-with-closed-eyes.jpg?s=612x612&w=0&k=20&c=EgPzzLN-eVPcIy09D84EM6NZxpOMwk6zdTRTQuSi4Pc=",
            "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=800&q=80", # Tech
            "https://media.istockphoto.com/id/2200128716/photo/ai-powers-big-data-analysis-and-automation-workflows-showcasing-neural-networks-and-data.jpg?s=612x612&w=0&k=20&c=z7kdn14AJhMX8JlenABkc3mT-df-V0JhxJzqnQ8Q81w=",
            "https://media.istockphoto.com/id/2226813113/photo/robotic-students-using-a-digital-tablet-while-operating-a-production-line-robot.jpg?s=612x612&w=0&k=20&c=HYILiLneHhrOBQuBlBVFqnCuRyN49L-JeJ0un_0IcZI=",
            "https://media.istockphoto.com/id/2223043330/photo/digital-road-digital-code-road-concept-3d-illustration.jpg?s=612x612&w=0&k=20&c=1pBEIR7ikPI1JNfZZEMGHlHBkFONhixsdSUT0IBOqx0=",
            "https://media.istockphoto.com/id/2221411629/photo/investor-reviewing-stock-reports-and-financial-dashboards-on-hybrid-tablet-laptop-with-ai.jpg?s=612x612&w=0&k=20&c=cT_tGQ8E55vfynSULnI6wDWGPdA-n6BtC8lvWQYVDrE=",
        ]

        # 2. Generate 27 more events to make 30 total
        for _ in range(27):
            events_data.append({
                "price": random.randint(500, 5000),
                "event_planner_name": fake.name(),
                "event_planner_contact": f"07{random.randint(10000000, 99999999)}", # Fake Kenyan number format
                "title": random.choice(event_titles),
                "image": random.choice(images),
                "description": fake.text(max_nb_chars=150),
                "location": random.choice(kenyan_locations),
                "age_limit": random.choice(["All ages", "18+", "21+"]),
                "capacity": random.randint(100, 10000),
                "date": fake.date_time_between(start_date='now', end_date='+90d', tzinfo=timezone.utc),
                "sponsor": random.choice(sponsors_list)
            })

        # Saving events to the database
        created_events = []
        for e_data in events_data:
            # We pop the sponsor out so we can pass the rest as kwargs
            event_sponsor = e_data.pop("sponsor")
            event = Event.objects.create(
                user=user,
                sponsor=event_sponsor,
                **e_data
            )
            created_events.append(event)

        # Create Speakers (Attached to your first 3 specific events)
        Speaker.objects.create(
            name="Stephen Hawking", email="stephen.h@speaker.com", event=created_events[0],
            organisation="STEPHEN HAWKING FOUNDATION", job_title="Founding Father", image="base64_string_here"
        )
        Speaker.objects.create(
            name="Bien", email="Bien@speaker.com", event=created_events[1],
            organisation="SAUTI SOL", job_title="Musician", image="base64_string_here"
        )
        Speaker.objects.create(
            name="Uhuru Kenyatta", email="kenyatta@speaker.com", event=created_events[2],
            organisation="CHARITY FOUNDATION", job_title="CEO", image="base64_string_here"
        )

        # Create Attendees
        user2 = User.objects.create_user(username="david", email="david@mail.com", password="password", age=25, gender="Male")
        user3 = User.objects.create_user(username="jenny", email="jenny@mail.com", password="password", age=22, gender="Female")

        Attendee.objects.create(name="Samantha Lee", email="samanthalee@example.com", user=user, event=created_events[2])
        Attendee.objects.create(name="David Kim", email="davidkim@example.com", user=user2, event=created_events[0])
        Attendee.objects.create(name="Jennifer Chen", email="jenniferchen@example.com", user=user3, event=created_events[2])

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with 30 events!'))