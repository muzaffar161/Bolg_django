from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from blog.models import Article, AuthorProfile, Category, Comment, Tag


CATEGORIES = [
    ("Cinema", "Reviews, premieres and the craft behind the camera.", "#f59e0b"),
    ("Sport", "Matchdays, athletes and the stories beyond the score.", "#22c55e"),
    ("Culture", "The ideas shaping how we watch and play.", "#6366f1"),
    ("Interviews", "Conversations with the people in the spotlight.", "#ec4899"),
]

TAGS = [
    "review",
    "premiere",
    "training",
    "champions",
    "behind-the-scenes",
    "opinion",
    "interview",
    "culture",
]

ARTICLES = [
    {
        "title": "Interstellar: ten years of reaching beyond the stars",
        "category": "Cinema",
        "tags": ["review", "behind-the-scenes"],
        "image": "article_covers/interstellar.jpg",
        "excerpt": "Why Nolan's space epic still feels like a personal letter to curiosity, family and the people we leave behind.",
        "body": "A decade after its release, Interstellar still occupies a strange place in popular cinema: a blockbuster that trusts silence, patience and scientific detail.\n\nThe film works because the spectacle never replaces the emotional centre. The docking sequence, the ice planet and the tesseract are memorable not because they are loud, but because every visual idea serves a father's promise to his daughter.\n\nRewatching it today, the practical effects hold up remarkably well. The restrained score gives the vastness room to breathe, and the final act turns theoretical physics into something deeply human. It is a reminder that the best science fiction is really about the size of our affection.",
        "author": "aisha",
        "featured": True,
    },
    {
        "title": "Dune: Part Two and the art of the enormous frame",
        "category": "Cinema",
        "tags": ["review", "premiere"],
        "image": "article_covers/dune-part-two.jpg",
        "excerpt": "Desert, dust and destiny: how Villeneuve turned a sci-fi novel into a tactile cinematic event.",
        "body": "Dune: Part Two is constructed on a scale that rarely feels excessive. Every wide shot of Arrakis carries weight because the camera stays long enough for us to understand the geography of power.\n\nThe sound design deserves as much attention as the imagery. The low, physical rumble of the sandworms makes the desert feel alive long before it appears on screen.\n\nWhat lingers is the ambiguity. Paul's journey is framed as a triumph and a warning at the same time, and the film refuses to resolve that tension neatly.",
        "author": "aisha",
        "featured": True,
    },
    {
        "title": "Parasite: the staircase as a social map",
        "category": "Cinema",
        "tags": ["review", "culture"],
        "image": "article_covers/parasite.jpg",
        "excerpt": "A closer look at the vertical architecture that makes Bong Joon-ho's thriller so brutally legible.",
        "body": "Every movement in Parasite is a movement up or down. The Kim family climbs the stairs toward the Parks' home; the housekeeper descends into the floodlit basement.\n\nThe staircase is not decoration. It is the film's argument made physical: the distance between two households is measured in steps, not in kilometres.\n\nThat clarity is why the famous dinner scene feels so explosive. The politeness on the surface cannot hide the geography underneath it.",
        "author": "omar",
        "featured": False,
    },
    {
        "title": "La La Land: the bittersweet beauty of a near miss",
        "category": "Cinema",
        "tags": ["review", "opinion"],
        "image": "article_covers/la-la-land.jpg",
        "excerpt": "The ending is not a trick. It is a mature admission that love and timing are separate things.",
        "body": "La La Land looks like a classical musical until it quietly stops being one. The colours, the waltz and the tap dancing belong to an older Hollywood grammar, but the final act belongs to adulthood.\n\nThe famous alternate-life montage works because it never erases what came before. Both futures are real in the emotional logic of the film.\n\nThat is the point: a relationship can be valuable without being permanent.",
        "author": "aisha",
        "featured": False,
    },
    {
        "title": "The morning routine of a marathoner",
        "category": "Sport",
        "tags": ["training", "champions"],
        "image": "article_covers/mia-chen.jpg",
        "excerpt": "What a 42-kilometre race actually asks of your boring, ordinary Tuesday morning.",
        "body": "The public image of marathon training is built on long runs and dramatic finishes. The real work happens on ordinary mornings, in the repeatable hours nobody photographs.\n\nConsistency beats intensity during a base phase. Easy kilometres, sleep and a disciplined warm-up are unglamorous, but they are what allow the hard sessions to produce adaptation instead of injury.\n\nA good week leaves you slightly hungry for the next one, not desperate for rest.",
        "author": "mia",
        "featured": True,
    },
    {
        "title": "Recovery is training: the case for doing less",
        "category": "Sport",
        "tags": ["training", "opinion"],
        "image": "article_covers/leo-martinez.jpg",
        "excerpt": "Muscles grow between sessions, not during them. Why the rest day deserves a place in your plan.",
        "body": "Athletes often treat a rest day as a failure of discipline. Physiologically, it is the opposite: the adaptation produced by a hard session happens during the hours that follow it.\n\nSleep, low-intensity movement and adequate calories are not accessories. They are the mechanisms that turn stress into progress.\n\nIf every week feels harder than the last, the answer may not be another workout.",
        "author": "leo",
        "featured": False,
    },
    {
        "title": "From the stands: why the derby never gets old",
        "category": "Sport",
        "tags": ["champions", "culture"],
        "image": "article_covers/daniel-brooks.jpg",
        "excerpt": "Ninety minutes, two streets and a competition that no table can explain.",
        "body": "A derby ignores the league table. Form, statistics and rational expectations stay at the gate.\n\nWhat makes these matches endure is their intimacy. The people on the pitch grew up near the people in the stands, and every tackle is read as a statement about belonging.\n\nThat is why the noise matters. It is not background; it is the second team on the field.",
        "author": "omar",
        "featured": False,
    },
    {
        "title": "A goalkeeper's guide to staying calm",
        "category": "Interviews",
        "tags": ["interview", "training"],
        "image": "article_covers/sofia-rossi.jpg",
        "excerpt": "Sofia Rossi on visualization, routine and the two seconds after a mistake.",
        "body": "You prepare for the mistake before it happens. The routine after a conceded goal has to be automatic: breathe, reset, find the next instruction.\n\nFilm study helps, but not in the way people expect. I do not watch to remember every shot. I watch to recognise the Movement before it becomes a shot.\n\nThe calm you see on television is mostly boring repetition away from it.",
        "author": "mia",
        "featured": False,
    },
    {
        "title": "Cinema and sport have more in common than you think",
        "category": "Culture",
        "tags": ["culture", "opinion"],
        "image": "article_covers/dune-part-two.jpg",
        "excerpt": "Both disciplines turn attention into emotion, and both depend on the courage to leave space.",
        "body": "A great match and a great film share an economy of attention. The camera and the crowd tell you where to look, but the meaning arrives in the pause that follows.\n\nSport has the advantage of uncertainty: no screenplay can guarantee the final ten minutes. Cinema has the advantage of control: every frame can be composed to carry memory.\n\nWhen the two meet, we remember the moment not as information but as a feeling.",
        "author": "aisha",
        "featured": False,
    },
]


class Command(BaseCommand):
    help = "Fill the blog with demo categories, tags, authors, articles and comments."

    def handle(self, *args, **options):
        if Article.objects.exists():
            self.stdout.write("Demo data already exists. Nothing to do.")
            return

        category_map = {}
        for name, description, accent in CATEGORIES:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": description, "accent": accent},
            )
            category_map[name] = category

        tag_map = {}
        for name in TAGS:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_map[name] = tag

        author_map = {}
        for username, email, first_name, last_name, bio, avatar in [
            (
                "aisha",
                "aisha@example.com",
                "Aisha",
                "Karimova",
                "Film critic. I write about images, memory and the long shadow of a good ending.",
                "author_avatars/aisha-karimova.jpg",
            ),
            (
                "mia",
                "mia@example.com",
                "Mia",
                "Chen",
                "Distance runner and coach. Believer in easy miles and hard questions.",
                "author_avatars/mia-chen.jpg",
            ),
            (
                "omar",
                "omar@example.com",
                "Omar",
                "Hassan",
                "Sports journalist covering derbies, tactics and the people behind the noise.",
                "author_avatars/omar-hassan.jpg",
            ),
            (
                "leo",
                "leo@example.com",
                "Leo",
                "Martinez",
                "Strength coach writing about recovery, habit and unglamorous progress.",
                "author_avatars/leo-martinez.jpg",
            ),
        ]:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "first_name": first_name, "last_name": last_name},
            )
            if created:
                user.set_password("demo12345")
                user.save()

            profile, _ = AuthorProfile.objects.get_or_create(user=user)
            profile.bio = bio
            profile.avatar = avatar
            profile.save()
            author_map[username] = user

        for item in ARTICLES:
            article = Article.objects.create(
                author=author_map[item["author"]],
                category=category_map[item["category"]],
                title=item["title"],
                excerpt=item["excerpt"],
                body=item["body"],
                image=item["image"],
                status=Article.STATUS_PUBLISHED,
                is_featured=item["featured"],
                views=120 + len(item["title"]) * 7,
            )
            article.tags.set([tag_map[name] for name in item["tags"]])

        first_article = Article.objects.first()
        Comment.objects.create(
            article=first_article,
            author=author_map["omar"],
            body="The detail about the emotional centre is exactly why this film stays with people.",
        )
        Comment.objects.create(
            article=first_article,
            author=author_map["mia"],
            body="A wonderful read. I had forgotten how restrained the score is in the quiet scenes.",
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {Category.objects.count()} categories, "
                f"{Tag.objects.count()} tags, {Article.objects.count()} articles "
                f"and {Comment.objects.count()} comments."
            )
        )
