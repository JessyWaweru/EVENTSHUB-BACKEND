

from django.core.management.base import BaseCommand
from datetime import timezone
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
                "location": "Workable Nairobi",
                "age_limit": "12+",
                "capacity": 500, 
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 2000, 
                "event_planner_name": 'Jessica Pear',
                "event_planner_contact": '0777263352',
                "title": "Music Festival",
                "image": "https://images.pexels.com/photos/2263436/pexels-photo-2263436.jpeg",
                "description": "Join us for a day of music, food, and fun!",
                "location": "DNM EVENTS PARK, Nairobi",
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
                "event_planner_name":"Captain Mann Bungoma",
                "event_planner_contact":"0703263326",
                "title":"Jude's birthday party",
                "image": "https://media.istockphoto.com/id/2191575922/photo/multiethnic-friends-company-in-carnival-wear-blowing-in-party-pipes-having-fun.jpg?s=612x612&w=0&k=20&c=bZgLVmiL7J9tg-tmVV72oECHi1d6gpSFZMn8whalzwI=",
                "description": "It is that time of the year.We are back.Jude the influencer is hosting an exclusive party at his beach house in Diani.All are welcomed .At a price.",
                "location": "Brookhaven Gardens, Nairobi",
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
                "image":"https://media.istockphoto.com/id/1718782607/photo/top-view-background-of-cozy-dinner-table-set-for-thanksgiving.jpg?s=612x612&w=0&k=20&c=0wbr7QazSa_X2gpxlx2MNlRJ7Tj-My9bTiYy0V4rmds=",
                "location": "Brookhaven Gardens, Nairobi",
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
                "location": "Sarit Center, Nairobi", 
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
                "image": "https://media.istockphoto.com/id/912547822/photo/shes-got-big-plans-to-run-the-city.jpg?s=612x612&w=0&k=20&c=M5_sOhbQMgc4I6heaL9fpjVrMwgKRU0sbI2YSeRToxM=",
                "description": "The Women CEOs Forum is a convention of like-minded women entrepreneurs, enterprise leaders and support organizations from various industries across Africa. The participants will come together to discuss their ambitions, goals, and challenges in the business environment.",
                "location": "Sarit Center,Nairobi", 
                "age_limit": "18+", 
                "capacity": 510,
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 0, 
                "event_planner_name": 'Jessy Njoroge', 
                "event_planner_contact": '0703261126',
                "title": "Sauti JENGE OPEN MIC",
                "description": "JENGE Kulture is a Pan African social change initiative that promotes a culture of social concern and creative, innovative action across the continent. We connect and support Africa’s Creators, Innovators and Changemakers and their work in creating and sustaining social change in Africa",
                "location": "JENGE Kulture, Nairobi", 
                "age_limit": "18+", 
                "image": "https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F502451239%2F545458234983%2F1%2Foriginal.20230427-155313?w=940&auto=format%2Ccompress&q=75&sharp=10&rect=0%2C0%2C3000%2C1500&s=66b44a9655179da3c31b60014dfa3f6c",
                "capacity": 200,
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 3500, 
                "event_planner_name": 'Mike Muchiri', 
                "event_planner_contact": '0713261126',
                "title": "CyFrica 2026 - Kenya",
                "description": "With the launch of the National Cybersecurity Strategy by the Government of Kenya, there is a need for more collaborative efforts between the public and private sectors to mitigate the emerging threat landscape. To facilitate such collaborations and bring together the best-in-class cybersecurity experts, Tradepass is hosting CyFrica in Nairobi, Kenya on 18 – 19 July 2023. The event will attract 600+ pre-qualified cybersecurity experts including the Heads of Information Security, Risk, Compliance, Forensics and Cyber Law from the leading public and private enterprises across the country.",
                "location": "KICC, Nairobi", 
                "age_limit": "18+", 
                "image": "https://media.istockphoto.com/id/1484313578/photo/cyber-security-network-data-protection-privacy-concept.jpg?s=612x612&w=0&k=20&c=mBkwneErmbHd7s8xauDNU-uXitNSXXBtxJ7C9He0Y9s=",
                "capacity": 100,
                "date": fake.date_time_between(start_date='now', end_date='+5d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 4000, 
                "event_planner_name": 'Harvey Spectre', 
                "event_planner_contact": '0745261126',
                "title": "Book Club",
                "description": "We are pleased to introduce our Book Club!\n\n  Each month we’ll announce a new pick of a book (or a part of it) that we’ll read right alongside you and other readers. The books we read will span a range of topics — from spiritualism, philosophy, history, religion, relationships, healthy living, science, and more.",
                "location": "Meridian Hotel Conference Centre, Nairobi", 
                "age_limit": "15+", 
                "image": "https://media.istockphoto.com/id/2148803754/photo/old-used-books-hardback-books-close-up.jpg?s=612x612&w=0&k=20&c=JuhjNB48DfMbX_P7GUl43EwxgadywFNgqpbXpUQsvdE=",
                "capacity": 30,
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 3000,
                "event_planner_name": 'Ala Baptista',
                "event_planner_contact": '0722121200',
                "title": "13th AMSUN SCIENTIFIC CONFERENCE",
                "description": "Exploring frontiers of Medicine through diversified research.",
                "location": "Chandaria Center for Performing Arts, Nairobi",
                "age_limit": "21+",
                "image": "https://media.istockphoto.com/id/1304697797/photo/african-american-man-presenting-at-medical-seminar.jpg?s=612x612&w=0&k=20&c=93V-E8ov0-6_fBNZ-iQKAGRmRWqM2Tqtf76R-vn7wEE=",
                "capacity": 500,
                "date": fake.date_time_between(start_date='now', end_date='+5d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 5000,
                "event_planner_name": 'Icks Moringa',
                "event_planner_contact": '0703263326',
                "title": "Web Hosting and Domain Names: Everything You Need to Know",
                "description": "Are you looking to start your own website or online business? In this event, we will cover everything you need to know about web hosting and domain names. We'll discuss the different types of hosting available, how to choose the right hosting for your website, and the importance of domain names in building your online brand.",
                "location": "Paradise Hall, Nairobi",
                "age_limit": "16+",
                "image": "https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F423964689%2F1347219007203%2F1%2Flogo.20230113-084337?w=940&auto=format%2Ccompress&q=75&sharp=10&s=62224c76edc2233694986a41066ebe2f",
                "capacity": 100,
                "date": fake.date_time_between(start_date='now', end_date='+5d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                "price": 1000,
                "event_planner_name": 'Milka Waweru',
                "event_planner_contact": '0730261126',
                "title": "We The Medicine - Healing Our Inner Child 2026. Guided Meditation.",
                "description": "Here you will find a community of souls who are searching to be all that they can, to awaken and remember their inner source of power, love.\n\nTogether we will be holding space to share loving kindness meditations and learn new skills and empowerment tools to help deal with PTSD, anxiety, depression, fear & childhood traumas.",
                "location": "Brookhaven Gardens, Nairobi",
                "age_limit": "18+",
                "image": "https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F192974469%2F124429251107%2F1%2Foriginal.20211129-000629?w=940&auto=format%2Ccompress&q=75&sharp=10&rect=0%2C83%2C794%2C397&s=6a7d05d396a86a7d5f27aca6cff06222",
                "capacity": 200,
                "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                
                "price": 2200,
                "event_planner_name": 'Jackie Rhoades',
                "event_planner_contact": '0703262226',
                "title": "Annual Rave Kenya",
                "description": "You know what you are signing up for!",
                "location": "Brookhaven Gardens, Nairobi",
                "age_limit": "26+",
                "image": "https://media.istockphoto.com/id/1913125761/photo/silhouettes-of-people-dancing-and-rising-hands-at-open-air-summer-festival.jpg?s=612x612&w=0&k=20&c=HqEoqMCPEyOR4uhOnc03sDONY267HJqwXcqTMZjqqPw=",
                "date": fake.date_time_between(start_date='now', end_date='+5d', tzinfo=timezone.utc),
                "sponsor": sponsor2,
                "capacity": 500
            },
            {
                
                "price": 2500,
                "event_planner_name": 'Irungu Ireri',
                "event_planner_contact": '0703261162',
                "title": "Mandonga vs Wanyonyi 2: Repeat or Revenge",
                "image": "https://media.istockphoto.com/id/1346093951/photo/shot-of-boxing-gloves-ready-to-be-used.jpg?s=612x612&w=0&k=20&c=Wq2XcJIRLh4lVlVI2MQzrfBjrpxMIe1emS01NnSvx7U=",
                "description": "---Mandonga vs Wanyonyi 2 - Repeat or Revenge---\n\nWill Mandonga confirm his January Victory or will Wanyonyi avenge that defeat.\n\nFans will be treated to an 8 fight bonanza on the night featuring 4 East African countries namely DRC, Tanzania, Uganda and hosts Kenya.",
                "location": "Paradise Gardens, Nairobi",
                "age_limit": "18+",
                "capacity": 500,
                "date": fake.date_time_between(start_date='now', end_date='+25d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                
                "price": 2000,
                "event_planner_name": 'Jessy Waweru',
                "event_planner_contact": '0703261126',
                "title": "Kike Neuro - Soul With Patience Shalom",
                "image": "https://images.unsplash.com/photo-1644596666688-c088a43ab500?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmV1cm9kaXZlcmdlbnQlMjBtdXNpY3xlbnwwfHwwfHx8MA%3D%3D",
                "description": "100% Kenyan music, and creatives living off their art.Run by a team of neurodivergent adults, our vision is an inclusive world that acknowledges, accommodates, values, includes and embraces neurodiversity.",
                "location": "Sweet Memories Gardens, Nairobi",
                "age_limit": "16+",
                "capacity": 5500,
                "date": fake.date_time_between(start_date='now', end_date='+25d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
              
                "price": 10000,
                "event_planner_name": 'Jessy Waweru',
                "event_planner_contact": '0703261126',
                "title": "DIAMOND PLATNUMZ LIVE ",
                "image": "https://images.unsplash.com/photo-1608637273739-15f0cd97285e?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8ZGlhbW9uZHxlbnwwfHwwfHx8MA%3D%3D",
                "description": "You know how it goes with SIMBA!Performing live with Arya as a feature.DO NOT MISS OUT!",
                "location": "The Carnivore Grounds, Nairobi",
                "age_limit": "25+",
                "capacity": 55500,
                "date": fake.date_time_between(start_date='now', end_date='+25d', tzinfo=timezone.utc),
                "sponsor": sponsor2
                
            },
            {
                
                "price": 2500,
                "event_planner_name": 'Jess Weru',
                "event_planner_contact": '0703621126',
                "title": "Head to Head Motorkhana",
                "image": "https://plus.unsplash.com/premium_photo-1661963826911-f369fa24c1a6?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8bW90b3IlMjByYWNpbmd8ZW58MHx8MHx8fDA%3D",
                "description": "Delta Motorsport and Club TT presents: The 3rd Edition of the Kenya National Tarmac Championship",
                "location": "Paco Thrill Haven, Naivasha",
                "age_limit": "25+",
                "capacity": 55500,
                "date": fake.date_time_between(start_date='now', end_date='+25d', tzinfo=timezone.utc),
                "sponsor": sponsor2
        
            },
            {
        
                "price": 5000,
                "event_planner_name": 'Jessica Alba',
                "event_planner_contact": '0722245122',
                "title": "The Sunday Braai",
                "image": "https://images.unsplash.com/photo-1613244665771-e8a2af4214af?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGJyYWFpfGVufDB8fDB8fHww",
                "description": "l'Equipe Choque Presents. The Sunday Braai\n- Where South and West African food meet -\n\nLadies and gentlemen we present to you the THIRD iteration of The Sunday Braai, after the overwhelming success of the last edition we invite you to join us on the 16th of July as we fire up our grills, stock up our bar and press play on a fantastic Sunday.",
                "location": " Village Market",
                "age_limit": "15+",
                "capacity": 100,
                "date": fake.date_time_between(start_date='now', end_date='+25d', tzinfo=timezone.utc),
                "sponsor": sponsor2
            },
            {
                
                "price": 2000,
                "event_planner_name": 'Jessy Waweru',
                "event_planner_contact": '0703261126',
                "title": "Afro-Coustic with Atemi Oyungu",
                "image": "https://plus.unsplash.com/premium_photo-1705351823609-deec7d4ef58f?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YWZybyUyMG11c2ljfGVufDB8fDB8fHww",
                "description": "This lovely event dubbed Afro-coustic will feature Atemi alongside talented artists Lisa Oduor-Noah, Kendi Nkonge, and Manasseh Shalom. Experience a preview of Atemi's new music and enjoy her beloved songs from her extensive catalog..",
                "location": " Sax & Violins Lounge, Karen",
                "age_limit": "25+",
                "capacity": 500,
                "date": fake.date_time_between(start_date='now', end_date='+25d', tzinfo=timezone.utc),
                "sponsor": sponsor2
        
    }
             
        ]

      
       
       
      

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