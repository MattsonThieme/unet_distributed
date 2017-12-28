BASE = "/home/bduser/unet/data/"
DATA_PATH = BASE+"/slices"
OUT_PATH  = BASE+"slices/Results/"
IMG_ROWS = 128
IMG_COLS = 128  
RESCALE_FACTOR = 1
SLICE_BY = 5 
BLOCKTIME = 0
NUM_INTRA_THREADS = 40
NUM_INTER_THREADS = 2
BATCH_SIZE = 512
IN_CHANNEL_NO = 1
OUT_CHANNEL_NO = 1

EPOCHS = 10

LEARNINGRATE = 0.0003  #0.005
DECAY_STEPS = 350
LR_FRACTION = 0.2

MODEL_FN = "brainWholeTumor" #Name for Mode=1
#MODEL_FN = "brainActiveTumor" #Name for Mode=2
#MODEL_FN = "brainCoreTumor" #Name for Mode=3

#Use flair to identify the entire tumor: test reaches 0.78-0.80: MODE=1
#Use T1 Post to identify the active tumor: test reaches 0.65-0.75: MODE=2
#Use T2 to identify the active core (necrosis, enhancing, non-enh): test reaches 0.5-0.55: MODE=3
MODE=1

# Important that these are ordered correctly: [0] = chief node, [1] = worker node, etc.
PS_HOSTS = ["10.100.68.245"]
PS_PORTS = ["2222"]
WORKER_HOSTS = ["10.100.68.193","10.100.68.183","10.100.68.185","10.100.68.187"]
WORKER_PORTS = ["2222", "2222", "2222", "2222"]

CHECKPOINT_DIRECTORY = "checkpoints/"