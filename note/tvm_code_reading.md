>源码相对比较比较难,要弄懂c++和python相互调用,packedfunc,Module,以及通过注册来实现加载
#Python安装解析
cd python; python setup.py install 安装方式,
注意==path = "tvm/_ffi/_cython"==
```python

    if "--inplace" in sys.argv: #python setup.py build_ext --inplace 会编译成动态库(so)
        from distutils.core import setup
        from distutils.extension import Extension
    else:
        from setuptools import setup#setuptools 功能比distutils更强大
        from setuptools.extension import Extension
    def config_cython():
        """Try to configure cython and return cython configuration"""
        if os.name == 'nt':
            print("WARNING: Cython is not supported on Windows, will compile without cython module")
            return []
        sys_cflags = sysconfig.get_config_var("CFLAGS")

        if "i386" in sys_cflags and "x86_64" in sys_cflags:
            print("WARNING: Cython library may not be compiled correctly with both i386 and x64")
            return []
        try:
            from Cython.Build import cythonize
            # from setuptools.extension import Extension
            if sys.version_info >= (3, 0):
                subdir = "_cy3"
            else:
                subdir = "_cy2"
            ret = []
            path = "tvm/_ffi/_cython"
            if os.name == 'nt':
                library_dirs = ['tvm', '../build/Release', '../build']
                libraries = ['libtvm']
            else:
                library_dirs = None
                libraries = None
            for fn in os.listdir(path):
                if not fn.endswith(".pyx"): #排除 core.cpp是生成的
                    continue
                ret.append(Extension(
                    "tvm._ffi.%s.%s" % (subdir, fn[:-4]),
                    ["tvm/_ffi/_cython/%s" % fn],#对应的库
                    include_dirs=["../include/",
                                "../3rdparty/dmlc-core/include",
                                "../3rdparty/dlpack/include",
                    ],
                    library_dirs=library_dirs,
                    libraries=libraries,
                    language="c++"))
            return cythonize(ret, compiler_directives={"language_level": 3})
        except ImportError:
            print("WARNING: Cython is not installed, will compile without cython module")
            return []
    setup(name='tvm', #python层面的包(import tvm)
        version=__version__,
        description="TVM: An End to End Tensor IR/DSL Stack for Deep Learning Systems",
        zip_safe=False,
        install_requires=[
            'numpy',
            'decorator',
            'attrs',
            'psutil',
            ],
        packages=find_packages(),
        distclass=BinaryDistribution,
        url='https://github.com/dmlc/tvm',
        ext_modules=config_cython(),
        **setup_kwargs)
```


Ctype方式,然后直接在python中调用c++

其他方式
Pybind11 参考文档Python - C++ bindings  Hardik Patel.png 
Pyrex :pyx文件包含pyi文件(内部定函数义cdef )

    cdef extern from "tvm/runtime/c_runtime_api.h":
        ctypedef struct DLDataType:
            uint8_t code
            uint8_t bits
            uint16_t lanes

https://openmc.readthedocs.io/en/stable/pythonapi/capi.html
https://intermediate-and-advanced-software-carpentry.readthedocs.io/en/latest/c++-wrapping.html
#tvm源码阅读
https://docs.tvm.ai/dev/codebase_walkthrough.html

    src - 
    src/relay 
    python - Python frontend that wraps C++ functions and objects implemented in src.
    topi - 计算定义和nn调度

Tvm/src

- common: Internal common utilities.
- api: API function registration.
- lang: The definition of DSL related data structure.
- arithmetic: Arithmetic expression and set simplification.
- op: The detail implementations about each operation(compute, scan, placeholder).
- schedule: The operations on the schedule graph before converting to IR.
- pass: The optimization pass on the IR structure.
- codegen: The code generator.
- runtime: Minimum runtime related codes.
- autotvm: The auto-tuning module.
- relay: Implementation of Relay. The second generation of NNVM, a new IR for deep learning frameworks.
- contrib: Contrib extension libraries.

##PackedFunc
class PackedFunc {std::function}: incubator-tvm/include/tvm/runtime/packed_func.h 
std::function 是一种通用的多态函数包装器 。std::function 的实例可以存储、复制和调用任何可调用的目标——函数、lambda表达式、绑定表达式或其他函数对象，以及指向成员函数的指针和指向数据成员的指针（统称为“可调用对象”）。

    /*!
    * \def NNVM_REGISTER_OP
    * \brief Register a new operator, or set attribute of the corresponding op.
    *
    * \param OpName The name of registry
    *
    * \code
    *
    * NNVM_REGISTER_OP(add)
    * .describe("add two inputs together")
    * .set_num_inputs(2)
    * .set_attr<OpKernel>("gpu_kernel", AddKernel);
    *
    * \endcode
    */
    #define NNVM_REGISTER_OP(OpName) \
    DMLC_STR_CONCAT(NNVM_REGISTER_VAR_DEF(OpName), __COUNTER__) = \
    ::dmlc::Registry<::nnvm::Op>::Get()->__REGISTER_OR_GET__(#OpName)

    friend class dmlc::Registry<Op>;
    Namespace
    lib = ctypes.CDLL(lib_path[0], ctypes.RTLD_GLOBAL)

lib_path[0]即为libtvm_runtime.so

##Module 
也是PackedFunc,z作为不同target的compiled obj
The PackedFunc and Module system also makes it easy to ship the function into remote devices directly

##Python调用c++

    #include <tvm/runtime/packed_func.h>
    void MyAdd(TVMArgs args, TVMRetValue* rv) {
    // automatically convert arguments to desired type.
    int a = args[0];
    int b = args[1];
    // automatically assign value return to rv
    *rv = a + b;
    }

    void CallPacked() {
    PackedFunc myadd = PackedFunc(MyAdd);
    // get back 3
    int c = myadd(1, 2);
    }

explicit PackedFunc(FType body) : body_(body) {}

注册

    // register a global packed function in c++
    TVM_REGISTER_GLOBAL("myadd").set_body(MyAdd);

调用

    import tvm
    myadd = tvm.get_global_func("myadd")# prints 3print(myadd(1, 2))

在上面的示例代码中，我们定义了PackedFunc函数MyAdd。它带有两个参数：args表示输入参数和rv表示返回值。这个函数是无类型的，没有必要严格限制输入参数和返回值的类型。只需要在调用PackedFunc函数时，把输入参数打包到TVMArgs类型数据中，并且从TVMRetValue类型数据中获取返回值。

得益于C++的模板函数技巧，我们可以像调用普通函数一样来调用PackedFunc类型函数。因为PackedFunc类型函数是无类型的，所以Python语言无需古怪的语法就可以调用PackedFunc函数。下面通过示例来展示：

    TVM_REGISTER_GLOBAL("module._PackImportsToLLVM")

Tvm.get_global_func再使用
```python
    def get_global_func(name, allow_missing=False):
        """Get a global function by name”””
        handle = FunctionHandle() #//FunctionHandle = ctypes.c_void_p

        check_call(_LIB.TVMFuncGetGlobal(c_str(name), ctypes.byref(handle)))
        if handle.value:
            return Function(handle, False)

        if allow_missing:
            return None

        raise ValueError("Cannot find global function %s" % name)

    def _load_lib():
        """Load libary by searching possible path."""
        lib_path = libinfo.find_lib_path()
        lib = ctypes.CDLL(lib_path[0], ctypes.RTLD_LOCAL)
        # DMatrix functions
        lib.NNGetLastError.restype = ctypes.c_char_p
        return lib
    class FunctionBase(object):
        """Function base."""
        __slots__ = ["handle", "is_global"]
        # pylint: disable=no-member
        def __init__(self, handle, is_global):
            """Initialize the function with handle

            Parameters
            ----------
            handle : FunctionHandle
                the handle to the underlying function.

            is_global : bool
                Whether this is a global function in python
            """
            self.handle = handle
            self.is_global = is_global

        def __del__(self):
            if not self.is_global and _LIB is not None:
                if _LIB.TVMFuncFree(self.handle) != 0:
                    raise get_last_ffi_error()

        def __call__(self, *args):
            """Call the function with positional arguments

            args : list
            The positional arguments to the function call.
            """
            temp_args = []
            values, tcodes, num_args = _make_tvm_args(args, temp_args)
            ret_val = TVMValue()
            ret_tcode = ctypes.c_int()
            if _LIB.TVMFuncCall(
                    self.handle, values, tcodes, ctypes.c_int(num_args),
                    ctypes.byref(ret_val), ctypes.byref(ret_tcode)) != 0:
                raise get_last_ffi_error()
            _ = temp_args
            _ = args
            return RETURN_SWITCH[ret_tcode.value](ret_val)
```

##C++调用python
==因为PackedFunc可以传递PackedFunc类型的参数，所以我们可以把函数从Python函数传递到C++
==TVM_REGISTER_GLOBAL("callhello")
.set_body([](TVMArgs args, TVMRetValue* rv) {
PackedFunc f = args[0];
f("hello world");
});==

    import tvm

    def callback(msg):#//python函数
    print(msg)

    # convert to PackedFunc
    f = tvm.convert(callback)
    callhello = tvm.get_global_func("callhello")
    # prints hello world
    callhello(f)

然后c中使用
static const PackedFunc& fbuild = GetPackedFunc("nnvm.compiler.build_target");



##Python层动态注册C++

@tvm.register_func("nnvm.compiler.build_target")


>from tvm import relay
加载tvm的__init__.py
加载relay 下的__init__.py
from .build_module import build 此时会加载build_module.py的import(from . import _build_module)
调用build_modul,内容为
    from tvm._ffi.function import _init_api    (target_module_name=tvm.relay._build_module)
```python
    def _init_api(namespace, target_module_name=None):
        """Initialize api for a given module name

        namespace : str
        The namespace of the source registry

        target_module_name : str
        The target module name if different from namespace
        """
        target_module_name = (
            target_module_name if target_module_name else namespace)

        _init_api_prefix(target_module_name, namespace)
```

参数为tvm.relay._build_module,relay.build_module

```python
    def _init_api_prefix(module_name, prefix):
        module = sys.modules[module_name]#//获取module_name对应的对象(包含模块文件路径)

        for name in list_global_func_names():
            if prefix == "api":
                fname = name
                if name.startswith("_"):
                    target_module = sys.modules["tvm._api_internal"]
                else:
                    target_module = module
            else:
                if not name.startswith(prefix):
                    continue
                fname = name[len(prefix)+1:]
                target_module = module

            if fname.find(".") != -1:
                continue
            f = get_global_func(name)#//获取全局函数并设置属性,也会调用check_call
            ff = _get_api(f)
            ff.__name__ = fname
            ff.__doc__ = ("TVM PackedFunc %s. " % fname)
            setattr(target_module, ff.__name__, ff)
            这里没有返回结果是因为已经注册为全局函数,所有后面直接用
```

==list_global_func_names()会调用	,得到已经注册的函数name	
check_call(_LIB.TVMFuncListGlobalNames(ctypes.byref(size),
                                           ctypes.byref(plist)))==

#运行流程
##网络解析
    mod, params = relay.testing.resnet.get_workload(
        num_layers=18, batch_size=batch_size, image_shape=image_shape)
    # relay def net structure and convert to relay.func -> relay.func
    # mod = relay.Module.from_expr(net)

Net是relay定义的网络结构(net : tvm.relay.Function) 再转化为relay.Module
这里用relay的op定义的,然后调用c++

    mod = relay.Module.from_expr(net),参数随机初始化, expr to pass def ,input IR
    return _module.Module_FromExpr(expr, funcs, defs)
    mod = relay.transform.InferType()(mod) retrun pass ,Infer the type of an expr

接着调用c上的代码
Binary file ./build/libtvm.so 有Module_FromExpr
定义在
./src/relay/ir/module.cc:TVM_REGISTER_API("relay._module.Module_FromExpr")
```c
    TVM_REGISTER_API("relay._module.Module_FromExpr")
    .set_body_typed<
    Module(Expr,
            tvm::Map<GlobalVar, Function>,
            tvm::Map<GlobalTypeVar, TypeData>)>([](Expr e,
                                                    tvm::Map<GlobalVar, Function> funcs,
                                                    tvm::Map<GlobalTypeVar, TypeData> type_defs) {
                                                return ModuleNode::FromExpr(e, funcs, type_defs);
                                                });
```

mod : tvm.Module 
./include/tvm/api_registry.h:#define TVM_REGISTER_API(OpName) TVM_REGISTER_GLOBAL(OpName)
模板


然后
with relay.build_config(opt_level=opt_level):
    graph, lib, params = relay.build_module.build(
        mod, target, params=params)

with relay.build_config(opt_level=opt_level):

    PassContext
    def __enter__(self):
        _transform.EnterPassContext(self)
        return self

    def __exit__(self, ptype, value, trace):
        _transform.ExitPassContext(self)


Build完毕会生成后端代码
func = mod["main"] #//mod : tvm.Module,

    # If current dispatch context is fallback context (the default root context),
    # then load pre-tuned parameters from TopHub
    if isinstance(autotvm.DispatchContext.current, autotvm.FallbackContext):
        tophub_context = autotvm.tophub.context(list(target.values()))
    else:
        tophub_context = autotvm.util.EmptyContext()

    with tophub_context:
        bld_mod = BuildModule()
        graph_json, mod, params = bld_mod.build(func, target, target_host, params)
    return graph_json, mod, params

BuildModule
==定义在./src/relay/backend/build_module.cc:TVM_REGISTER_GLOBAL("relay.build_module._BuildModule")==
```python
    class BuildModule(object):
        """Build a Relay function to run on TVM graph runtime. This class is used
        to expose the `RelayBuildModule` APIs implemented in C++.
        """
        def __init__(self):
            self.mod = _build_module._BuildModule()
    

        self._get_graph_json = self.mod["get_graph_json"]#//实现了__getitem__
        self._get_module = self.mod["get_module"]
        self._build = self.mod["build"]
        self._set_params_func = self.mod["set_params"]
        self._get_params_func = self.mod["get_params"]

    def build(self, func, target=None, target_host=None, params=None):
        """
        Parameters
        ----------
        func: relay.Function
            The function to build.
        Returns
        -------
        graph_json : str
            The json string that can be accepted by graph runtime.

        mod : tvm.Module
            The module containing necessary libraries.

        params : dict
            The parameters of the final graph.
        """
        target = _update_target(target)

        # Setup the params.
        if params:
            self._set_params(params)
        # Build the function
        self._build(func, target, target_host)
        # Get artifacts
        graph_json = self.get_json()
        mod = self.get_module()
        params = self.get_params()
```



ModuleBase调用

python/tvm/_ffi/function.py
```python
    class ModuleBase(object):
        """Base class for module"""
        __slots__ = ["handle", "_entry", "entry_name"]

        def __init__(self, handle):
            self.handle = handle
            self._entry = None
            self.entry_name = "__tvm_main__"

        def __del__(self):
            check_call(_LIB.TVMModFree(self.handle))

        @property
        def entry_func(self):
            """Get the entry function

            Returns
            -------
            f : Function
                The entry function if exist
            """
            if self._entry:
                return self._entry
            self._entry = self.get_function(self.entry_name)
            return self._entry

        def get_function(self, name, query_imports=False):
            """Get function from the module.

            Parameters
            ----------
            name : str
                The name of the function

            query_imports : bool
                Whether also query modules imported by this module.

            Returns
            -------
            f : Function
                The result function.
            """
            ret_handle = FunctionHandle()
            check_call(_LIB.TVMModGetFunction(
                self.handle, c_str(name),
                ctypes.c_int(query_imports),
                ctypes.byref(ret_handle)))
            if not ret_handle.value:
                raise AttributeError(
                    "Module has no function '%s'" %  name)
            return Function(ret_handle, False)

        def import_module(self, module):
            """Add module to the import list of current one.

            Parameters
            ----------
            module : Module
                The other module.
            """
            check_call(_LIB.TVMModImport(self.handle, module.handle))

        def __getitem__(self, name):
            if not isinstance(name, string_types):
                raise ValueError("Can only take string as function name")
            return self.get_function(name)
    凡是在类中定义了这个__getitem__ 方法，那么它的实例对象（假定为p），可以像这样p[key] 取值，当实例对象做p[key] 运算时，会调用类中的方法__getitem__。


    def __call__(self, *args):
        if self._entry:
            return self._entry(*args)
        f = self.entry_func
        return f(*args)

--------


    def register_func(func_name, f=None, override=False):
        """Register global function

        Parameters
        ----------
        func_name : str or function
            The function name

        f : function, optional
            The function to be registered.

        override: boolean optional
            Whether override existing entry.

        Returns
        -------
        fregister : function
            Register function if f is not specified.

        Examples
        --------
        The following code registers my_packed_func as global function.
        Note that we simply get it back from global function table to invoke
        it from python side. However, we can also invoke the same function
        from C++ backend, or in the compiled TVM code.

        .. code-block:: python

        targs = (10, 10.0, "hello")
        @tvm.register_func
        def my_packed_func(*args):
            assert(tuple(args) == targs)
            return 10
        # Get it out from global function table
        f = tvm.get_global_func("my_packed_func")
        assert isinstance(f, tvm.nd.Function)
        y = f(*targs)
        assert y == 10
        """
        if callable(func_name):
            f = func_name
            func_name = f.__name__

        if not isinstance(func_name, str):
            raise ValueError("expect string function name")

        ioverride = ctypes.c_int(override)
        def register(myf):
            """internal register function"""
            if not isinstance(myf, Function):
                myf = convert_to_tvm_func(myf)
            check_call(_LIB.TVMFuncRegisterGlobal(
                c_str(func_name), myf.handle, ioverride))
            return myf
        if f:
            return register(f)
        return register
```
------------------------
```python
    def get_global_func(name, allow_missing=False):
        """Get a global function by name

        Parameters
        ----------
        name : str
            The name of the global function

        allow_missing : bool
            Whether allow missing function or raise an error.

        Returns
        -------
        func : tvm.Function
            The function to be returned, None if function is missing.
        """
        handle = FunctionHandle()
        check_call(_LIB.TVMFuncGetGlobal(c_str(name), ctypes.byref(handle)))
        if handle.value:
            return Function(handle, False)

        if allow_missing:
            return None

        raise ValueError("Cannot find global function %s" % name)
```

##其他定义
    定义函数
    n = tvm.var("n")
    A = tvm.placeholder((n,), name='A')     
    //return _api_internal._Placeholder(shape, dtype, name)#//./src/api/api_lang.cc:TVM_REGISTER_API("_Placeholder"),然后就可以直接使用

    其中tensorrt定义在这几个地方
    python/tvm/tensor.py 
    include/tvm/tensor.h
    src/lang/tensor.cc

    tvm.tensor.Tensor
    @register_object
    class Tensor(Object, _expr.ExprOp):
        """Tensor object, to construct, see function.Tensor"""

        def __call__(self, *indices):
        
    B = tvm.placeholder((n,), name='B')
    d=a+c
    C = tvm.compute(A.shape, lambda i: A[i] + B[i], name="C")
    s = tvm.create_schedule(C.op)
    print(tvm.lower(s, [a,b], simple_mode=True))生成人类可读的代码
    bx, tx = s[C].split(C.op.axis[0], factor=64)
    fadd = tvm.build(s, [A, B, C], tgt, target_host=tgt_host, name="myadd") 
    relay.build(...)
    1 通过查询op register 获取op的实现
    2 生成计算表达式和op调度
    3 编译op到target code
    print(mod.astext(show_meta_data=False))#//生成IR
    查看生成的代码(目标机器上)
    if tgt == "cuda" or tgt == "rocm" or tgt.startswith('opencl'):
        dev_module = fadd.imported_modules[0]
        print("-----GPU code-----")
        print(dev_module.get_source('asm'))
    else:
        print(fadd.get_source())
	

使用

    ctx = tvm.context(tgt, 0)
    n = 1024
    a = tvm.nd.array(np.random.uniform(size=n).astype(A.dtype), ctx)
    b = tvm.nd.array(np.random.uniform(size=n).astype(B.dtype), ctx)
    c = tvm.nd.array(np.zeros(n, dtype=C.dtype), ctx)
    fadd(a, b, c)
    tvm.testing.assert_allclose(c.asnumpy(), a.asnumpy() + b.asnumpy())


创建装在共享库

    cc.create_shared(temp.relpath("myadd.so"), [temp.relpath("myadd.o")])
    fadd1 = tvm.runtime.load_module(temp.relpath("myadd.so"))
导出一个库

    fadd.export_library(temp.relpath("myadd_pack.so"))