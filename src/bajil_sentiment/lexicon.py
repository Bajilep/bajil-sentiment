"""Weighted sentiment vocabulary."""


def _split_words(text):
    return text.split()


def build_lexicon():
    groups = {
        4.0: _split_words("""
            amazing awesome brilliant excellent exceptional fantastic flawless
            incredible magnificent outstanding perfect phenomenal remarkable
            sensational spectacular superb terrific thrilled triumphant wonderful
            wow best love loved delightful extraordinary gorgeous ideal
            masterpiece miraculous breathtaking
        """),

        3.0: _split_words("""
            great admirable adorable appreciate appreciated beautiful cheerful
            commendable confident congratulations cool creative enjoyable excited
            exciting fabulous favorable favourite favorite friendly fun generous
            glad grateful happy helpful impressive inspiring joyful kind lovely
            marvelous marvellous optimistic pleased positive proud recommend
            recommended reliable satisfying satisfied smooth strong success
            successful superior talented useful valuable vibrant win winner
            winning worthwhile pleasurable refreshing dependable trustworthy
        """),

        2.0: _split_words("""
            acceptable agree agreeable benefit beneficial better bright capable
            comfortable convenient decent effective efficient encouraging enjoy
            enjoyed entertaining fair fast fortunate fresh good hopeful improved
            improving interesting like liked lively nice pleasant promising quality
            safe smart stable supportive sweet thanks thankful worthy accurate
            affordable clean easy elegant flexible genuine innovative neat
            productive quick responsive secure skillful solid welcoming works
            worked progress improvement advantage advantages
        """),

        1.0: _split_words("""
            calm clear correct enough okay ok prepared ready reasonable simple
            suitable timely welcome balanced available complete consistent normal
            practical satisfactory fine peaceful proper steady adequate manageable
            pass passed solved solution solutions usable valid warm
        """),

        -1.0: _split_words("""
            average concern concerned inconvenient limited low minor ordinary
            questionable sadly shortage small strange uncertain unclear unexpected
            unknown annoying awkward basic bothered delay doubt doubtful dull
            lacking nervous odd restricted scarce upset inconvenience
        """),

        -2.0: _split_words("""
            bad buggy careless complaint complaints confusing difficult dirty
            dislike disliked expensive fear flawed glitch hard incorrect issue
            issues late lazy mediocre missing noisy offensive regret regretted risky
            rough slow sorry suspicious tired trouble troubling uncomfortable unfair
            unhappy unpleasant unsafe unstable warning worry worried wrong inaccurate
            inadequate incomplete inconsistent ineffective inefficient overpriced
            unreliable weak limitation limitations malfunction malfunctions
            dissatisfied
        """),

        -3.0: _split_words("""
            angry boring corrupt cruel damaged dead defective delayed disappointed
            disappointing disaster error fake frustrating furious harmful hopeless
            inferior misleading nasty negative painful poor problem problems
            rejected ridiculous rude sad sick stolen stressful stupid ugly waste
            abusive alarmed chaotic cheated depressed disturbing embarrassed faulty
            fearful greedy guilty hostile ignored impossible insulting irritating
            miserable ruined shameful shocking
        """),

        -4.0: _split_words("""
            atrocious awful broken catastrophic disgusting dreadful fail failed
            failure garbage hate hated horrible horrific nightmare pathetic scam
            terrible toxic trash unacceptable unusable useless worst worthless
            abysmal disastrous disgraceful fraud fraudulent horrendous horrid
            infuriating outrageous revolting unbearable unforgivable appalling
            devastated devastating dangerous
        """),
    }

    lexicon = {}

    for score, words in groups.items():
        for word in words:
            lexicon[word] = score

    return lexicon