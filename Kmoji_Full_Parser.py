#K-Moji Full Parser
#DICTIONARIES
VERTICAL_EYES = {
    "o": "awake/surprised",
    "O": "very-wide/shock/very-surprised",
    "0": "acute-shock/extremely-surprised",
    ".": "blank/confused/lagging/brain-fried",
    "-": "bored/disappointed/tired/sleepy/unamused/unpleasant/reluctant",
    "^": "joy/happy/chipper/positive",
    "U": "gentle/sleepy/satisifed",
    "V": "heavy/solemnity/closed-off/quiet-sorrow",
    "=": "comfortable/soft/sleepy/annoyed",
    ";": "nervous/worried/anxious/bashful/shy/uncertain",
    "@": "dizzy/overwhelmed/confused/flustered/frazzled",
    "e": "ew/unpleasant/ick/not-good/cringe/disgust",
    "T": "soft-crying/sad/whyyy",
    "*": "star-eyed-excitement",
    "x": "dead/I'm-toast/x-eyes",
    "Q": "crying/sad/shocked-crying/whyyy",
    "Y": "crying/heavier-crying/withdrawn-while-crying/quiet-sorrow-crying/solemnity-crying"
}
VERTICAL_MOUTHS = {
    "u": "happy/content/joy",
    "v": "happy/content/joy",
    "o": "surprise/oh/woah",
    "O": "very-surprised/woahhh",
    "-": "Disappointed/ugh/blank",
    "_": "Disappointed/ugh/blank",
    "A": "surprise/shock/omg/oh-no",
    "w": "playful/mischievous/happy/cute/gremlin-energy/slightly-feral",
    "^": "sad/unpleasnt/unhappy",
    "3": "playful/mischief/silly/cute/goofy",
    ">": "confusion/blank/brain-fried/dumb/what?/lagging",
    "~": "nervous/unsure/maybe/indecisive",
    "Q": "drooling/lagging/brain-fried/I-don't-get-it/What?/stupefied",
    "y": "silly/happy/derpy/tongue-blep/playful/unserious/teasing",
    ",..,": "fanged-teeth/creature-mouth/feral"
}
VERTICAL_INTERNAL_SLOT_PARTICLES = {
    "///": "blushing"
}
HORIZONTAL_EYES = {
    ":": "neutral/blank",
    "B": "cool/smug",
    "8": "shock/surprise/omg",
    ";": "playfulness/cute/mischievous/thoughtful",
    "x": "excited/too much" #FLAG: maybe add X capital as more emphasis and note that in Syntax system 1.0.8 somehow... Capitals was a thing I was working on...
}
#have a way to distinguish modifiers from Mouths that are similar ex ); also figure out how to distinguish between horizontal and vertical stuff > probably some form of identifying the structure of the two systems
HORIZONTAL_MOUTHS = {
    "3": "playful/mischievous/cute/happy/adorable/silly",
    ")": "happy/content", #similar to modifier  idea: Use the Horizontal structure to identify whether its modifier or mouth aka (Modifier + Eyes + optional tear + Mouth) EX. > in slot 0 = modifier > after eyes = mouth
    "(": "sad/unhappy", #similar to modifier
    "]": "smug happy/mischievous smug",
    "[": "smug unhappy/mischievous smug",
    "B": "thinking/stupefied/lagging",
    "P": "playful/silly/blank mouth silly",
    "b": "playful/silly/blank mouth silly", #Alt of P mouth
    "|": "neutral/blank expression/disappoint",
    "l": "neutral/blank expression/disappoint", #Alt of | mouth
    "I": "neutral/blank expression/disappoint", #2nd Alt of | mouth
    "/": "whatever/eh/uncaring/it is what it is",
    "o": "oh/surprise/shock/woah",
    "U": "silly neutral/goofy neutral",
    "V": "confused neutral/huh?",
    "L": "disgust/unhappy/upset/annoyed/Mad",
    "C": "very sad/very disappointed/very unhappy",
    "T": "well I told you so/Yep/Uhuh/blank expression",
    "Y": "well I told you so/Yep/Uhuh/blank expression", #Alt of T mouth
    ">": "mischievous happy/acute happy", #similar to modifiers
    "<": "mischievous unhappy/acute unhappy", # similar to modifiers
    "D": "happy/excited/hype" #SPECIAL MOUTH. CAN FOLLOW LAM RULE TO BE sad/distressed/frustrated, figure that out
}
HORIZONTAL_MODIFIERS = {
    ">": "anger/annoyance/aggressive/pushing",
    "<": "sad/shy/retreating/leaning back",
    ")": "frustrated/annoyed/upset/mischievous",
    "(": "soft sad/sad surprise/worry/melancholy"
}
HORIZONTAL_INTERNAL_SLOT_PARTICLES = {
    "'": "a single tear"
}
#FUNCTIONS
def detect_modifiers(kmoji):
    modifier_notes = []

    # Check for ;; (swet/anxiety/panic)
    if kmoji.endswith(";;;;"):
        modifier_notes.append("severe anxiety/severe nervousness/severe panick/severe sweating")
        kmoji = kmoji[:-4]
    elif kmoji.endswith(";;"):
        modifier_notes.append("anxious/nervous/panicked/sweating")
        kmoji = kmoji[:-2] #trim ;; off the end

    # Check for ## or # (anger vein - count them)
    if kmoji.endswith("##"):
        modifier_notes.append("fuming/rage")
        kmoji = kmoji[:-2]
    elif kmoji.endswith("#"):
        modifier_notes.append("angry/irritated/annoyed")
        kmoji = kmoji[:-1]

    return kmoji, modifier_notes
def parse_directional_eyes(left_eye, right_eye):
    if left_eye == ">" and right_eye == "<":
        return "excited/too-much/intense"
    elif left_eye == "<" and right_eye == ">":
        return "sad/tired/down/melancholic/depressed/unwell"
    elif left_eye == ">" and right_eye == ">":
        return "suspicion/judgement/side-eye/playful-shade"
    elif left_eye == "<" and right_eye == "<":
        return "suspicion/judgement/side-eye/playful-shade"
    else:
        return "unknown-directional-combination"
# Check for blush particle
def parse_vertical(kmoji):#VERTICAL PARSER
    kmoji, modifier_notes = detect_modifiers(kmoji)
    blush = False #default is false for blush just in case until proven true so we don't error out
    if "///" in kmoji: #CHeck if blush exists in Kmoji
        blush = True
        parts = kmoji.split("///") #if blush is true then we use the split function to cut out the /// from the Kmoji leaving us with eye mouth eye parts
        left_eye = parts[0]
        mouth = parts[1]
        right_eye = parts[2]
    elif ",..," in kmoji: #checking for RMSC mouth is important because this can make the kmoji structure wonky
        left_eye = kmoji[0]
        right_eye = kmoji[-1] #add the [-1] so we tell the right eye to go to the very back of the kmoji in slot order, regardless of how many slots there are since RMSC is 4 characters
        mouth = ",..,"
    elif len(kmoji) == 2 and kmoji[0] in "<>" and kmoji[1] in "<>": #Fixes a crash if there is no mouth for kmoji at length 2 that has <> in it by telling it there is no slot 2, just 0 & 1 and mouth is nothing
        left_eye = kmoji[0]
        right_eye = kmoji[1]
        mouth = ""
    else:
        left_eye = kmoji[0] #The regular Kmoji structure
        mouth = kmoji[1]
        right_eye = kmoji[2]
    # Look up meanings
    if left_eye in "<>" and right_eye in "<>": #This if statement determines directional eyes
        left_eye_meaning = parse_directional_eyes(left_eye, right_eye)
        right_eye_meaning = "" #The reason "" is here for right eye meaning is because >< only mean something when they're in a pair, so > or < on its own doesn't mean anything. So the left eye handles the look ups for both and the right eye is blank so it doesn't show the definition twice. 
    else:#Parse eyes normally if they don't have directions
        left_eye_meaning = VERTICAL_EYES.get(left_eye, "unknown-eye") #have "unknown-eye" because it's like excel's N/A so it just says if it can't find it then it's unkown so it doesn't crash the program.
        right_eye_meaning = VERTICAL_EYES.get(right_eye, "unknown-eye")

    mouth_meaning = VERTICAL_MOUTHS.get(mouth, "unknown-mouth") #Parse mouth normally

    if mouth == "": #Polsih; just means if the mouth is nothing then the mouth meaning should be empty
        mouth_meaning = ""

    blush_str = " | Blush: blushing" if blush else "" #Blush string in a ternary expression (squished if else) so blush string definition is |: blushing if blush (is true) otherwise write nothing "" (false)
    modifier_str = f" | Modifiers: {', '.join(modifier_notes)}" if modifier_notes else "" #Tacks on modifier meaning in the format description and ', '.join just means you'll see commas between each modifier notes meaning and its also a ternary expression

    if right_eye_meaning == "" and mouth_meaning == "": # Polish; if right eye is nothing and mouth meaning is nothing then basically don't add right eye or Mouth in the final returned answer
        return f"Eyes: {left_eye_meaning}{blush_str}{modifier_str}"
    elif right_eye_meaning == "":
        return f"Eyes: {left_eye_meaning} | Mouth: {mouth_meaning} {blush_str}{modifier_str}" #if the right eye meaning is "" blank then just return the meaning of the left eyes (noted as Eyes for both), mouth, blush, and modifiers in the established format
    else: 
        return f"Left Eye: {left_eye_meaning} | Mouth: {mouth_meaning} | Right Eye: {right_eye_meaning}{blush_str}{modifier_str}" #if the left & and right eye are different then return both of their meanings in the established format
def parse_horizontal(kmoji): #HORIZONTAL PARSER
    #LAM RULE CHECK - LEFT ANCHORED MOUTH (D)
    if kmoji[0] == "D":
        mouth = "D"
        mouth_meaning = "sad/distressed/frustrated"
        kmoji = kmoji[1:]

        tear = None
        if len(kmoji) > 0 and kmoji[0] == "'":
            tear = kmoji[0]
            kmoji = kmoji[1:]

        eyes = kmoji[0]
        eyes_meaning = HORIZONTAL_EYES.get(eyes, "unknown-eyes")
        kmoji = kmoji[1:]
        
        modifier = None
        if len(kmoji) > 0 and kmoji[0] in HORIZONTAL_MODIFIERS:
            modifier = kmoji[0]
        modifier_meaning = HORIZONTAL_MODIFIERS.get(modifier, None)

        result = f"Eyes: {eyes_meaning} | Mouth: {mouth_meaning}"
        if modifier_meaning:
            result = result + f" | Modifier: {modifier_meaning}"
        if tear: 
            result = result.replace("Mouth:", "Tear: single tear | Mouth:")
        return result
    #NORMAL HORIZONTAL PARSING
    modifier = None
    
    # Step 1: Check for modifier at start
    if len(kmoji) > 0 and kmoji[0] in HORIZONTAL_MODIFIERS:
        modifier = kmoji[0]
        kmoji = kmoji[1:]
    
    modifier_meaning = HORIZONTAL_MODIFIERS.get(modifier, None)
    
    # Step 2: Extract eyes
    eyes = kmoji[0]
    kmoji = kmoji[1:]
    eyes_meaning = HORIZONTAL_EYES.get(eyes, "unknown-eyes")
    
    # Step 3: Check for optional tear
    tear = None
    if len(kmoji) > 0 and kmoji[0] == "'":
        tear = kmoji[0]
        kmoji = kmoji[1:]
    
    # Step 4: Extract mouth
    mouth = kmoji
    mouth_meaning = HORIZONTAL_MOUTHS.get(mouth, "unknown-mouth")
    
    # Step 5 & 6: Build output
    result = f"Eyes: {eyes_meaning} | Mouth: {mouth_meaning}"
    if modifier_meaning:
        result = f"Modifier: {modifier_meaning} | " + result
    if tear:
        result = result.replace("Mouth:", "Tear: single tear | Mouth:")
    
    return result
def parse_kmoji(kmoji) -> str: #K-moji Parser Router - routes to either Vertical or Horizontal parser for parsing
    #LAM Routing Check 
    if kmoji[0] == "D": # D is the only LAM mouth
        return parse_horizontal(kmoji)
    #REGULAR ROUTING CHECK
    if len(kmoji) == 2 and kmoji[0] in "<>" and kmoji[1] in "<>":
        return parse_vertical(kmoji)
    elif len(kmoji) == 2:
        return parse_horizontal(kmoji)
    elif len(kmoji) >= 3 and kmoji[1] in HORIZONTAL_EYES:
        return parse_horizontal(kmoji)
    else:
        return parse_vertical(kmoji)
#TESTS

print(parse_kmoji("Q///~///=#"))