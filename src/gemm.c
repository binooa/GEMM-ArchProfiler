#include "gemm.h"
#include "utils.h"
#include "cuda.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "gem5/m5ops.h"

static int gemm_counter = 0;

void gemm(int TA, int TB, int M, int N, int K, float ALPHA, 
        float *A, int lda, 
        float *B, int ldb,
        float BETA,
        float *C, int ldc)
{
    gemm_cpu( TA,  TB,  M, N, K, ALPHA,A,lda, B, ldb,BETA,C,ldc);
}

void gemm_nn(int M, int N, int K, float ALPHA, 
        float *A, int lda, 
        float *B, int ldb,
        float *C, int ldc)
{
    m5_checkpoint(0, 0);
    m5_reset_stats(0, 0); 
    
    int i, j, k; // Common variables used across implementations

    #ifdef GEMM_TILED
    int ii, jj, kk; // Variables for Tiled GEMM
    const int BLOCK_SIZE = 64; // Block size specific to Tiled GEMM
    #pragma omp parallel for collapse(2) private(ii, jj, kk, i, j, k)
    for (ii = 0; ii < M; ii += BLOCK_SIZE) {
        for (kk = 0; kk < K; kk += BLOCK_SIZE) {
            for (jj = 0; jj < N; jj += BLOCK_SIZE) {
                for (i = ii; i < ii + BLOCK_SIZE && i < M; ++i) {
                    for (k = kk; k < kk + BLOCK_SIZE && k < K; ++k) {
                        register float A_PART = ALPHA * A[i * lda + k];
                        for (j = jj; j < jj + BLOCK_SIZE && j < N; ++j) {
                            C[i * ldc + j] += A_PART * B[k * ldb + j];
                        }
                    }
                }
            }
        }
    }
    #elif defined(GEMM_OPTIMIZED)
    const int UNROLL_FACTOR = 4; // Unrolling factor specific to Optimized GEMM
    #pragma omp parallel for private(i, j, k)
    for (i = 0; i < M; ++i) {
        for (k = 0; k < K; ++k) {
            register float A_PART = ALPHA * A[i * lda + k];
            for (j = 0; j < N; j += UNROLL_FACTOR) {
                // Loop unrolling
                C[i * ldc + j] += A_PART * B[k * ldb + j];
                if (j + 1 < N) C[i * ldc + j + 1] += A_PART * B[k * ldb + j + 1];
                if (j + 2 < N) C[i * ldc + j + 2] += A_PART * B[k * ldb + j + 2];
                if (j + 3 < N) C[i * ldc + j + 3] += A_PART * B[k * ldb + j + 3];
            }
        }
    }
    #else
    // Default GEMM_NN implementation
    #pragma omp parallel for
    for (i = 0; i < M; ++i) {
        for (k = 0; k < K; ++k) {
            register float A_PART = ALPHA * A[i * lda + k];
            for (j = 0; j < N; ++j) {
                C[i * ldc + j] += A_PART * B[k * ldb + j];
            }
        }
    }
    #endif

    m5_dump_stats(0, 0);
    m5_exit(0);
}




void gemm_cpu(int TA, int TB, int M, int N, int K, float ALPHA, 
        float *A, int lda, 
        float *B, int ldb,
        float BETA,
        float *C, int ldc)
{
    gemm_counter++;
    printf("cpu: %d %d %d %d %d %f %d %d %f %d\n",TA, TB, M, N, K, ALPHA, lda, ldb, BETA, ldc);
    int i, j;
    for(i = 0; i < M; ++i){
        for(j = 0; j < N; ++j){
            C[i*ldc + j] *= BETA;
        }
    }
    if(!TA && !TB)
    {
        printf("gemm_nn called %d\n", gemm_counter );
        gemm_nn(M, N, K, ALPHA,A,lda, B, ldb,C,ldc);
    }
}

