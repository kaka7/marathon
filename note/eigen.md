
Eigen的设计思路,是把所有能优化的步骤放在编译时去优化 要想运行时变快,写Eigen代码的工程师需要显式地告诉Eigen矩阵的特性,告诉的越多,越能提供空间让编译器在编译时加速算法


Eigen并不是一步一步地先做转置,再去乘,而是使用lazy evaluation的方法 Lazy evalution,是把计算本身尽可能放在最后做,减少内存访问 在代码上来看,就是 transpose()函数并没有做转置,和operator*() 本身也没有做乘法,只是更新了一下flag,真正运行计算的是 operator+=()才做内存读取和计算
Dynamic就会用动态内存分配 所以在已知矩阵大小时应尽可能声明大小,比如Matrix<double, 10, 10> 如果内存在整个程序中大小会变,但知道最大可能的大小,都可以告知Eigen,Eigen同样会选择用静态内存
最后是内存的读写 Lazy evaluation的另一个特点是不生成中间变量,减少内存搬运次数,
而Eigen为了防止矩阵覆盖自己,对矩阵-矩阵乘法会生成一个中间变量 如果我们知道等式左右两边没有相同的项,则可以通知Eigen去取消中间变量 Hessian.noalias() += Jacobian i.transpose()* Jacobian j; 以上是普通稠密矩阵计算 如果矩阵本身有自身的性质,都可以通知Eigen,让Eigen用对应的加速方式 比如正定矩阵可以只用上三角进行计算,并且这个转换能够完成的前提是通过 CRTP实现的父类子类之间的⼀⼀对应。


固定大小的矩阵连续存储,For dynamic-size, the coefficients will be stored as a pointer to a dynamically-allocated array. Because of this, we need to abstract storage away from the Matrix class. That's DenseStorage,internal::aligned_new 如果支持SIMD就对齐分配多个,否则new

expression template.
the operator+ doesn't by itself perform any computation, it just returns an abstract "sum of vectors" expression.
这里我们不需要动态多态性，因为特征的整个设计是基于这样一个假设的:所有的复杂性和所有的抽象都是在编译时解决的。这是至关重要的:如果抽象不能在编译时得到解决，那么特征的编译时优化机制就会变得无用，更不用说如果抽象必须在运行时得到解决，那么它本身就会产生开销。
Curiously Recurring Template Pattern:In short, MatrixBase takes a template parametaber Derived. Whenever we define a subclass Subclass, we actually make Subclass inherit MatrixBase<Subclass>. 

Eigen默认使用OpenMP实现多线程并行运算，但并不是所有计算都是支持多线程的。在目前最新的Eigen 3.3.5中，支持多线程的函数有以下：

    稠密矩阵乘法
    PartialPivLU分解
    行优先稀疏矩阵 * 稠密矩阵(或稠密向量)
    共轭梯度求解器ConjugateGradient，其中UpLo模板参数必须为Lower|Upper
    使用行优先稀疏矩阵的BiCGSTAB
    最小二乘共轭梯度求解器LeastSquaresConjugateGradient


element-wise:A = B + C - D;
for (int i=0; i<n; i++)
  A[i] = B[i] + C[i] - D[i];

矩阵乘法:gemm
// catch A * B + Y and builds Y' + A' * B'
TreeOpt<Sum<Product<A,B>,Y> > { … };
// catch X + A * B + Y and builds (X' + Y') + (A' * B')
TreeOpt<Sum<Sum<X,Product<A,B> >,Y> > { … };

使用https://github.com/PacktPublishing/Hands-On-Machine-Learning-with-CPP/blob/master/Chapter08/eigen/eigen_recommender.cc

https://blog.csdn.net/xuezhisdc/article/details/54631490使用
http://eigen.tuxfamily.org/index.php?title=How_to_run_the_benchmark_suite
http://eigen.tuxfamily.org/index.php?title=Benchmark
http://gcdart.blogspot.com/2013/06/fast-matrix-multiply-and-ml.html 代码在https://github.com/gcdart/dense-matrix-mult/blob/master/EIGEN/dense_mult_eigen.cpp

sparse https://github.com/sofa-framework/sofa/blob/aa82deb90973ffcfeb707f9c92a3bb491bae513d/SofaKernel/modules/SofaDefaultType/SofaDefaultType_test/MapMapSparseMatrixEigenUtils_test.cpp
CONCLUSION 2013的

OpenBLAS seems to be the best library (atleast w.r.t to the machine I ran the tests on) for Dense-Dense matrix multiplication. It scales well with increasing number of cores as well as increasing size of matrices .

For multi-threaded applications,

OpenBLAS > MKL > ATLAS >> EIGEN > ACML

For single-threaded applications,

OpenBLAS ≈ ACML  > MKL > ATLAS >> EIGEN


May be next-time I will post some of the comparisons on Sparse-Dense matrix multiplication,

对于原本多线程的程序，最好定义宏EIGEN_DONT_PARALLELIZE （详见: Eigen and multi-threading）
EIGEN_DONT_PARALLELIZE宏定义关闭eigen的多线程。
如果程序本身使用了多线程，需要使用以下方式初始化eigen

#include <Eigen/Core>
int main(int argc, char** argv){ 
   Eigen::initParallel();  
   ...}

the effect of noalias() here is to bypass the evaluate-before-assigning flag.
MatrixXd m = MatrixXd::Random(3,3); 运行时分配空间 堆
Matrix3d m = Matrix3d::Random(); 编译时
MatrixXf a(10,15);
VectorXf b(30);
a is a 10x15 dynamic-size matrix, with allocated but currentlyuninicoeffib is a dynamic-size vector of size 30, with alloccurrentlyuninitialized coeffi
std::copy(M.data(),M.data()+M.size(),datamemcpy(data_memcopy,M.data(),M.size() * sizeof(double));
  

typedef Matrix<float, 4, 4> Matrix4f;
typedef Matrix<double, Dynamic, Dynamic> MatrixXd;
typedef Matrix<int, Dynamic, 1> VectorXi;
Matrix<float, 3, Dynamic>
A default constructor is always available, never performs any dynamic memory allocation, and never initializes the matrix coefficients.
Eigen::Map<Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor>> m2(v.data(), 3, 4);
void std_vector2eigen_matrix(Eigen::MatrixXd& r, Tensor2D& a)
{
    for (size_t i = 0; i < a.size(); i++)
    r.row(i) = Eigen::VectorXd::Map(&a[i][0], a[i].size());
}

    Eigen::Map<Eigen::RowVectorXi> v_map(data, 4);

    https://github.com/PacktPublishing/Hands-On-Machine-Learning-with-CPP/blob/master/Chapter08/eigen/eigen_recommender.cc
 std::map<int, Eigen::Vector4f, std::less<int>,
Eigen::aligned_allocator<std::pair<const int, Eigen::Vector4f> > > 

Vector2d a(5.0, 6.0);
MatrixXd m(2,2);
m(0,0) = 3;
m << 1, 2, 3,
   4, 5, 6,
   7, 8, 9;
VectorXd v(2);
v(0) = 4;We restrict operator[] to vectors, 
syntax m(index) is not restricted to vectors, 
default to column-major storage order
All these methods are still available on fixed-size matrices, for the sakeof API uniformity.

不用显示分配内存
MatrixXf a(2,2);
std::cout << "a is of size " << a.rows() << "x" << a.cols() << std::endl;
MatrixXf b(3,3);
a = b;
resize

For small sizes, especially for sizes smaller than (roughly) 16, using fixedsizes is hugely beneficial to performance, as it allows Eigen to avoiddynamic memory allocation and to unroll loops. Internally, a fixed-size Eigenmatrix is just a plain array, i.e. doing
Matrix4f mymatrix; 等价于 float mymatrix[16]; 是在栈上分配
MatrixXf mymatrix(rows,columns); float *mymatrix = new float[rows*columns]; 不是常量就是动态大小在堆上分配  dynamic-size matrix is always allocated on the heap, 
大的空间(>32)在堆栈上的不同分配带来的收益差别不大

Matrix<float, 3, 3, RowMajor>
Matrix<typename Scalar,
       int RowsAtCompileTime,
       int ColsAtCompileTime,
       int Options = 0,
       int MaxRowsAtCompileTime = RowsAtCompileTime,
       int MaxColsAtCompileTime = ColsAtCompileTime>

a fixed upper bound is known at compile time. The biggest reason why you might want to do that is to avoid dynamic memory allocation

For fixed-size, the matrix coefficients are stored as a plain member array. For dynamic-size, the coefficients will be stored as a pointer to a dynamically-allocated array. Because of this, we need to abstract storage away from the Matrix class. That's DenseStorage

#include <Eigen/Core>
#include <iostream>
 
class MyVectorType : public Eigen::VectorXd
{
public:
    MyVectorType(void):Eigen::VectorXd() {}
 
    // This constructor allows you to construct MyVectorType from Eigen expressions
    template<typename OtherDerived>
    MyVectorType(const Eigen::MatrixBase<OtherDerived>& other)
        : Eigen::VectorXd(other)
    { }
 
    // This method allows you to assign Eigen expressions to MyVectorType
    template<typename OtherDerived>
    MyVectorType& operator=(const Eigen::MatrixBase <OtherDerived>& other)
    {
        this->Eigen::VectorXd::operator=(other);
        return *this;
    }
};
 
int main()
{
  MyVectorType v = MyVectorType::Ones(4);
  v(2) += 10;
  v = 2 * v;
  std::cout << v.transpose() << std::endl;
}
8 2 2 9 
9 1 4 4 
3 5 4 5 

8 2 2 9 9 1 4 4 3 5 4 5 
8 9 3 2 1 5 2 4 4 9 4 5 列存储:按照m的列依次存储,内存可以认为是一行一行的

// -fopenmp && OMP_NUM_THREADS=2
   omp_set_num_threads(3);//和OMP_NUM_THREADS意义一样
  cout << "thread num:" << Eigen::nbThreads() << endl;
//   initParallel();
//   setNbThreads(2);这两个参数只有当OMP激活后才生效


to Eigen
float* raw_data = malloc(...);
Map<MatrixXd> M(raw_data, rows, cols);
// use M as a MatrixXd
M = M.inverse();
• from Eigen
MatrixXd M;
float* raw_data = M.data();
int stride = M.outerStride();
raw_data[i+j*stride]

https://www.licc.tech/article?id=63

http://eigen.tuxfamily.org/dox/group__QuickRefPage.html
http://eigen.tuxfamily.org/dox/group__SparseQuickRefPage.html
// A simple quickref for Eigen. Add anything that's missing.
// Main author: Keir Mierle

关系

狭义的BLAS/LAPACK可理解为用于线性代数运算库的API
Netlib实现了Fortran/C版的BLAS/LAPACK、CBLAS/CLAPACK
开源社区及商业公司针对API实现了BLAS（ATLAS、OpenBLAS）和LAPACK（MKL、ACML、CUBLAS）的针对性优化
Eigen、Armadillo除自身实现线性代数运算库外还支持上述各种BLAS/LAPACK为基础的底层以加速运算

对比
备选：MKL、OpenBLAS、Eigen、Armadillo
接口易用程度：Eigen > Armadillo > MKL/OpenBLAS
速度：MKL≈OpenBLAS > Eigen(with MKL) > Eigen > Armadillo

其中：
OpenBLAS没有单核版本，强行指定OMP_NUM_THREADS=1性能损失大，不考虑
MKL直接使用学习成本较高，但是性能最强Armadillo效率和接口易用性不如Eigen
Eigen的原生BLAS/LAPACK实现速度不如MKL、OpenBLAS，但是使用MKL做后台性能和MKL原生几乎一样，所以可以视情况决定是否使用MKL

#include <Eigen/Dense>

Matrix<double, 3, 3> A;               // Fixed rows and cols. Same as Matrix3d.
Matrix<double, 3, Dynamic> B;         // Fixed rows, dynamic cols.
Matrix<double, Dynamic, Dynamic> C;   // Full dynamic. Same as MatrixXd.
Matrix<double, 3, 3, RowMajor> E;     // Row major; default is column-major.
Matrix3f P, Q, R;                     // 3x3 float matrix.
Vector3f x, y, z;                     // 3x1 float matrix.
RowVector3f a, b, c;                  // 1x3 float matrix.
VectorXd v;                           // Dynamic column vector of doubles
double s;                            

// Basic usage
// Eigen          // Matlab           // comments
x.size()          // length(x)        // vector size
C.rows()          // size(C,1)        // number of rows
C.cols()          // size(C,2)        // number of columns
x(i)              // x(i+1)           // Matlab is 1-based
C(i,j)            // C(i+1,j+1)       //

A.resize(4, 4);   // Runtime error if assertions are on.
B.resize(4, 9);   // Runtime error if assertions are on.
A.resize(3, 3);   // Ok; size didn't change.
B.resize(3, 9);   // Ok; only dynamic cols changed.
                  
A << 1, 2, 3,     // Initialize A. The elements can also be
     4, 5, 6,     // matrices, which are stacked along cols
     7, 8, 9;     // and then the rows are stacked.
B << A, A, A;     // B is three horizontally stacked A's.
A.fill(10);       // Fill A with all 10's.

// Eigen                                    // Matlab
MatrixXd::Identity(rows,cols)               // eye(rows,cols)
C.setIdentity(rows,cols)                    // C = eye(rows,cols)
MatrixXd::Zero(rows,cols)                   // zeros(rows,cols)
C.setZero(rows,cols)                        // C = zeros(rows,cols)
MatrixXd::Ones(rows,cols)                   // ones(rows,cols)
C.setOnes(rows,cols)                        // C = ones(rows,cols)
MatrixXd::Random(rows,cols)                 // rand(rows,cols)*2-1            // MatrixXd::Random returns uniform random numbers in (-1, 1).
C.setRandom(rows,cols)                      // C = rand(rows,cols)*2-1
VectorXd::LinSpaced(size,low,high)          // linspace(low,high,size)'
v.setLinSpaced(size,low,high)               // v = linspace(low,high,size)'
VectorXi::LinSpaced(((hi-low)/step)+1,      // low:step:hi
                    low,low+step*(size-1))  //


// Matrix slicing and blocks. All expressions listed here are read/write.
// Templated size versions are faster. Note that Matlab is 1-based (a size N
// vector is x(1)...x(N)).
// Eigen                           // Matlab
x.head(n)                          // x(1:n)
x.head<n>()                        // x(1:n)
x.tail(n)                          // x(end - n + 1: end)
x.tail<n>()                        // x(end - n + 1: end)
x.segment(i, n)                    // x(i+1 : i+n)
x.segment<n>(i)                    // x(i+1 : i+n)
P.block(i, j, rows, cols)          // P(i+1 : i+rows, j+1 : j+cols)
P.block<rows, cols>(i, j)          // P(i+1 : i+rows, j+1 : j+cols)
P.row(i)                           // P(i+1, :)
P.col(j)                           // P(:, j+1)
P.leftCols<cols>()                 // P(:, 1:cols)
P.leftCols(cols)                   // P(:, 1:cols)
P.middleCols<cols>(j)              // P(:, j+1:j+cols)
P.middleCols(j, cols)              // P(:, j+1:j+cols)
P.rightCols<cols>()                // P(:, end-cols+1:end)
P.rightCols(cols)                  // P(:, end-cols+1:end)
P.topRows<rows>()                  // P(1:rows, :)
P.topRows(rows)                    // P(1:rows, :)
P.middleRows<rows>(i)              // P(i+1:i+rows, :)
P.middleRows(i, rows)              // P(i+1:i+rows, :)
P.bottomRows<rows>()               // P(end-rows+1:end, :)
P.bottomRows(rows)                 // P(end-rows+1:end, :)
P.topLeftCorner(rows, cols)        // P(1:rows, 1:cols)
P.topRightCorner(rows, cols)       // P(1:rows, end-cols+1:end)
P.bottomLeftCorner(rows, cols)     // P(end-rows+1:end, 1:cols)
P.bottomRightCorner(rows, cols)    // P(end-rows+1:end, end-cols+1:end)
P.topLeftCorner<rows,cols>()       // P(1:rows, 1:cols)
P.topRightCorner<rows,cols>()      // P(1:rows, end-cols+1:end)
P.bottomLeftCorner<rows,cols>()    // P(end-rows+1:end, 1:cols)
P.bottomRightCorner<rows,cols>()   // P(end-rows+1:end, end-cols+1:end)

// Of particular note is Eigen's swap function which is highly optimized.
// Eigen                           // Matlab
R.row(i) = P.col(j);               // R(i, :) = P(:, j)
R.col(j1).swap(mat1.col(j2));      // R(:, [j1 j2]) = R(:, [j2, j1])

// Views, transpose, etc;
// Eigen                           // Matlab
R.adjoint()                        // R'
R.transpose()                      // R.' or conj(R')       // Read-write
R.diagonal()                       // diag(R)               // Read-write
x.asDiagonal()                     // diag(x)
R.transpose().colwise().reverse()  // rot90(R)              // Read-write
R.rowwise().reverse()              // fliplr(R)
R.colwise().reverse()              // flipud(R)
R.replicate(i,j)                   // repmat(P,i,j)


// All the same as Matlab, but matlab doesn't have *= style operators.
// Matrix-vector.  Matrix-matrix.   Matrix-scalar.
y  = M*x;          R  = P*Q;        R  = P*s;
a  = b*M;          R  = P - Q;      R  = s*P;
a *= M;            R  = P + Q;      R  = P/s;
                   R *= Q;          R  = s*P;
                   R += Q;          R *= s;
                   R -= Q;          R /= s;

// Vectorized operations on each element independently
// Eigen                       // Matlab
R = P.cwiseProduct(Q);         // R = P .* Q
R = P.array() * s.array();     // R = P .* s
R = P.cwiseQuotient(Q);        // R = P ./ Q
R = P.array() / Q.array();     // R = P ./ Q
R = P.array() + s.array();     // R = P + s
R = P.array() - s.array();     // R = P - s
R.array() += s;                // R = R + s
R.array() -= s;                // R = R - s
R.array() < Q.array();         // R < Q
R.array() <= Q.array();        // R <= Q
R.cwiseInverse();              // 1 ./ P
R.array().inverse();           // 1 ./ P
R.array().sin()                // sin(P)
R.array().cos()                // cos(P)
R.array().pow(s)               // P .^ s
R.array().square()             // P .^ 2
R.array().cube()               // P .^ 3
R.cwiseSqrt()                  // sqrt(P)
R.array().sqrt()               // sqrt(P)
R.array().exp()                // exp(P)
R.array().log()                // log(P)
R.cwiseMax(P)                  // max(R, P)
R.array().max(P.array())       // max(R, P)
R.cwiseMin(P)                  // min(R, P)
R.array().min(P.array())       // min(R, P)
R.cwiseAbs()                   // abs(P)
R.array().abs()                // abs(P)
R.cwiseAbs2()                  // abs(P.^2)
R.array().abs2()               // abs(P.^2)
(R.array() < s).select(P,Q );  // (R < s ? P : Q)
R = (Q.array()==0).select(P,R) // R(Q==0) = P(Q==0)
R = P.unaryExpr(ptr_fun(func)) // R = arrayfun(func, P)   // with: scalar func(const scalar &x);


// Reductions.
int r, c;
// Eigen                  // Matlab
R.minCoeff()              // min(R(:))
R.maxCoeff()              // max(R(:))
s = R.minCoeff(&r, &c)    // [s, i] = min(R(:)); [r, c] = ind2sub(size(R), i);
s = R.maxCoeff(&r, &c)    // [s, i] = max(R(:)); [r, c] = ind2sub(size(R), i);
R.sum()                   // sum(R(:))
R.colwise().sum()         // sum(R)
R.rowwise().sum()         // sum(R, 2) or sum(R')'
R.prod()                  // prod(R(:))
R.colwise().prod()        // prod(R)
R.rowwise().prod()        // prod(R, 2) or prod(R')'
R.trace()                 // trace(R)
R.all()                   // all(R(:))
R.colwise().all()         // all(R)
R.rowwise().all()         // all(R, 2)
R.any()                   // any(R(:))
R.colwise().any()         // any(R)
R.rowwise().any()         // any(R, 2)

// Dot products, norms, etc.
// Eigen                  // Matlab
x.norm()                  // norm(x).    Note that norm(R) doesn't work in Eigen.
x.squaredNorm()           // dot(x, x)   Note the equivalence is not true for complex
x.dot(y)                  // dot(x, y)
x.cross(y)                // cross(x, y) Requires #include <Eigen/Geometry>

//// Type conversion
// Eigen                  // Matlab
A.cast<double>();         // double(A)
A.cast<float>();          // single(A)
A.cast<int>();            // int32(A)
A.real();                 // real(A)
A.imag();                 // imag(A)
// if the original type equals destination type, no work is done

// Note that for most operations Eigen requires all operands to have the same type:
MatrixXf F = MatrixXf::Zero(3,3);
A += F;                // illegal in Eigen. In Matlab A = A+F is allowed
A += F.cast<double>(); // F converted to double and then added (generally, conversion happens on-the-fly)

// Eigen can map existing memory into Eigen matrices.
float array[3];
Vector3f::Map(array).fill(10);            // create a temporary Map over array and sets entries to 10
int data[4] = {1, 2, 3, 4};
Matrix2i mat2x2(data);                    // copies data into mat2x2
Matrix2i::Map(data) = 2*mat2x2;           // overwrite elements of data with 2*mat2x2
MatrixXi::Map(data, 2, 2) += mat2x2;      // adds mat2x2 to elements of data (alternative syntax if size is not know at compile time)

// Solve Ax = b. Result stored in x. Matlab: x = A \ b.
x = A.ldlt().solve(b));  // A sym. p.s.d.    #include <Eigen/Cholesky>
x = A.llt() .solve(b));  // A sym. p.d.      #include <Eigen/Cholesky>
x = A.lu()  .solve(b));  // Stable and fast. #include <Eigen/LU>
x = A.qr()  .solve(b));  // No pivoting.     #include <Eigen/QR>
x = A.svd() .solve(b));  // Stable, slowest. #include <Eigen/SVD>
// .ldlt() -> .matrixL() and .matrixD()
// .llt()  -> .matrixL()
// .lu()   -> .matrixL() and .matrixU()
// .qr()   -> .matrixQ() and .matrixR()
// .svd()  -> .matrixU(), .singularValues(), and .matrixV()

// Eigenvalue problems
// Eigen                          // Matlab
A.eigenvalues();                  // eig(A);
EigenSolver<Matrix3d> eig(A);     // [vec val] = eig(A)
eig.eigenvalues();                // diag(val)
eig.eigenvectors();               // vec
// For self-adjoint matrices use SelfAdjointEigenSolver<>

