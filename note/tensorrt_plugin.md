#uff_custom_plugin
TensorRT-5.0.2.6/samples/python/ 通过动态库的形式,另外一个例子fc_plugin_caffe_mnist 是Pybind11 caffe

lenet5.py 训练python层面的模型(可以使用relu6,也就是说tf python中已经有了relu6,这里训练处模型后,由于trt中没有relu6,所以要写插件)
mnist_uff_custom_plugin.py
>先加载动态库
 #Path where clip plugin library will be built (check README.md)
CLIP_PLUGIN_LIBRARY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'build/libclipplugin.so'
)

>然后定义一个node告知UffParser插件的名字和参数
    def prepare_namespace_plugin_map():
            # The "clipMin" and "clipMax" fields of this TensorFlow node will be parsed by createPlugin,
    import graphsurgeon as gs    
    trt_relu6 = gs.create_plugin_node(name="trt_relu6", op="CustomClipPlugin", clipMin=0.0, clipMax=6.0)
        namespace_plugin_map = {
            ModelData.RELU6_NAME: trt_relu6
        }
        return namespace_plugin_map

    namespace {
        static const char* CLIP_PLUGIN_VERSION{"1"};
        static const char* CLIP_PLUGIN_NAME{"CustomClipPlugin"};
    }
    class ClipPluginCreator : public IPluginCreator

初始化插件类,申明参数 clipMin,clipMax
ClipPluginCreator::ClipPluginCreator()
创建插件,具体实现

    IPluginV2* ClipPluginCreator::createPlugin
    for (int i = 0; i < fc->nbFields; i++){
        if (strcmp(fields[i].name, "clipMin") == 0) {
            assert(fields[i].type == PluginFieldType::kFLOAT32);
            clipMin = *(static_cast<const float*>(fields[i].data));
        } else if (strcmp(fields[i].name, "clipMax") == 0) {
            assert(fields[i].type == PluginFieldType::kFLOAT32);
            clipMax = *(static_cast<const float*>(fields[i].data));
        }
    }
    return new ClipPlugin(name, clipMin, clipMax);

ClipPlugin类

    REGISTER_TENSORRT_PLUGIN(ClipPluginCreator);注册,然后就可以使用了
    ClipPlugin::enqueue{clipInference ...使用clipMin, clipMax}
    最终cuda内的relu6实现的函数是
    clipInference
    int clipInference(
        cudaStream_t stream,
        int n,
        float clipMin,
        float clipMax,
        const void* input,
        void* output)
    {
        const int blockSize = 512;
        const int gridSize = (n + blockSize - 1) / blockSize;
        clipKernel<float, blockSize><<<gridSize, blockSize, 0, stream>>>(n, clipMin, clipMax, static_cast<const float*>(input),static_cast<float*>(output));
        return 0;
    }

总结:插件中实现好两个类(ClipPluginCreator,ClipPlugin)借口即可以及具体cuda实现