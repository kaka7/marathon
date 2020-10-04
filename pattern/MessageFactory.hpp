#pragma once
#include <map>
#include <string>
#include <functional>
#include <memory>
#include "Message.hpp"

/*
you can change the key type as integer.
    1提供一个单例工厂对象。
    2工厂注册对象（保存创建对象的key和构造器）。
    3利用辅助类，在辅助类对象的构造过程中实现目标对象地注册。
    4利用一个宏来生成辅助对象。
    5在派生类文件中调用这个宏实现自动注册。
*/
struct factory
{
	template<typename T>
	struct register_t//3 目标对象地注册,只保存构造函数,内部class可调用factory::get().map_
	{
		register_t(const std::string& key)
		{
			factory::get().map_.emplace(key, [] { return new T(); });
		}

		template<typename... Args>
		register_t(const std::string& key, Args... args)
		{
			factory::get().map_.emplace(key, [&] { return new T(args...); });
		}
	};

	static Message* produce(const std::string& key)
	{
		if (map_.find(key) == map_.end())
			throw std::invalid_argument("the message key is not exist!");

		return map_[key]();
	}

	static std::unique_ptr<Message> produce_unique(const std::string& key)
	{
		return std::unique_ptr<Message>(produce(key));
	}

	static std::shared_ptr<Message> produce_shared(const std::string& key)
	{
		return std::shared_ptr<Message>(produce(key));
	}

private:
	factory() {};//1
	factory(const factory&) = delete;
	factory(factory&&) = delete;

	static factory& get()//1 如果这里调用new产生obj(如createRunner),只会产生一次,即地址相同,如果实例化访问则要public
	{
		static factory instance;
		return instance;
	}

	static std::map<std::string, std::function<Message*()>> map_;//2
};

std::map<std::string, std::function<Message*()>> factory::map_;//2 这里体现构造函数而非对象

// 4 用宏来生成辅助对象,本质:全局的静态变量
#define REGISTER_MESSAGE_VNAME(T) reg_msg_##T##_
#define REGISTER_MESSAGE(T, key, ...) static factory::register_t<T> REGISTER_MESSAGE_VNAME(T)(key, ##__VA_ARGS__);