# Configuration Flags
GPU=0
CUDNN=0
OPENCV=0
OPENMP=0
DEBUG=0

VPATH=./src/:./examples
SLIB=libdarknet.so
ALIB=libdarknet.a
EXEC=darknet
OBJDIR=./obj/

CC=gcc
CPP=g++
AR=ar
ARFLAGS=rcs
OPTS=-Ofast
LDFLAGS=-lm -pthread -I/path/to/gem5/include -L/path/to/gem5/lib -lm5
COMMON=-Iinclude/ -Isrc/
CFLAGS=-Wall -Wfatal-errors -Wno-unused-result -Wno-unknown-pragmas -fPIC -Wno-stringop-truncation $(COMMON) -I/home/binu/gem5/gem5/include

# gem5-specific paths
GEM5_INCLUDE=/opt/GEMM-ArchProfiler/gem5/include
GEM5_LIB=/opt/GEMM-ArchProfiler/gem5/util/m5/build/x86/out

# Add gem5 paths to compilation and linking flags
CFLAGS+= -I$(GEM5_INCLUDE)
LDFLAGS+= -L$(GEM5_LIB) -lm5

# Multi-threading and GEMM Method Options
THREADING=
GEMM_METHOD=

ifeq ($(DEBUG), 1)
    OPTS=-O0 -g
endif

CFLAGS+=$(OPTS)

# Object Files
OBJ=gemm.o utils.o deconvolutional_layer.o convolutional_layer.o list.o image.o activations.o \
    im2col.o col2im.o blas.o crop_layer.o dropout_layer.o maxpool_layer.o softmax_layer.o data.o \
    matrix.o network.o connected_layer.o cost_layer.o parser.o option_list.o detection_layer.o \
    route_layer.o upsample_layer.o box.o normalization_layer.o avgpool_layer.o layer.o \
    local_layer.o shortcut_layer.o logistic_layer.o activation_layer.o rnn_layer.o gru_layer.o \
    crnn_layer.o demo.o batchnorm_layer.o region_layer.o reorg_layer.o tree.o lstm_layer.o \
    l2norm_layer.o yolo_layer.o iseg_layer.o image_opencv.o dummy_gpu.o


EXECOBJA=captcha.o lsd.o super.o art.o tag.o cifar.o go.o rnn.o segmenter.o regressor.o classifier.o \
    coco.o yolo.o detector.o nightmare.o instance-segmenter.o darknet.o

EXECOBJ=$(addprefix $(OBJDIR), $(EXECOBJA))
OBJS=$(addprefix $(OBJDIR), $(OBJ))
DEPS=$(wildcard src/*.h) Makefile include/darknet.h

# Menu for Compilation Options
.PHONY: menu clean all

menu:
	@echo "Select Threading Option:"
	@echo "1. Single-threaded"
	@echo "2. Multi-threaded (OpenMP)"
	@read threading_choice; \
	case $$threading_choice in \
		1) $(MAKE) threading THREADING=-DSINGLE_THREAD;; \
		2) $(MAKE) threading THREADING=-fopenmp;; \
		*) echo "Invalid choice! Aborting."; exit 1;; \
	esac

threading:
	@echo "Select GEMM Method:"
	@echo "1. Basic GEMM (gemm_nn)"
	@echo "2. Tiled GEMM"
	@echo "3. Optimized GEMM"
	@read gemm_choice; \
	case $$gemm_choice in \
		1) $(MAKE) all GEMM_METHOD=-DGEMM_NN;; \
		2) $(MAKE) all GEMM_METHOD=-DGEMM_TILED;; \
		3) $(MAKE) all GEMM_METHOD=-DGEMM_OPTIMIZED;; \
		*) echo "Invalid choice! Aborting."; exit 1;; \
	esac

# Configuration Flags
MAKEFLAGS += --no-print-directory


# Build Targets
all: obj compile link
	@echo "Compilation and Linking Successful: $(EXEC) has been created."

compile: $(EXECOBJ) $(OBJS)
	@echo "Compilation Step Completed."

link:
	$(CC) $(COMMON) $(CFLAGS) $(THREADING) $(GEMM_METHOD) $(EXECOBJ) $(OBJS) -o $(EXEC) $(LDFLAGS)

$(ALIB): $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

$(SLIB): $(OBJS)
	$(CC) $(CFLAGS) -shared $^ -o $@ $(LDFLAGS)

$(OBJDIR)%.o: %.cpp $(DEPS)
	$(CPP) $(COMMON) $(CFLAGS) -c $< -o $@

$(OBJDIR)%.o: %.c $(DEPS)
	$(CC) $(COMMON) $(CFLAGS) $(THREADING) $(GEMM_METHOD) -c $< -o $@

obj:
	mkdir -p $(OBJDIR)

clean:
	rm -rf $(OBJDIR) $(SLIB) $(ALIB) $(EXEC) results backup
