using System;
using System.IO;
using System.Text.Json;
using System.Collections.Generic;

namespace SettingsAccesser{
    public class SettingsOperations{
        private static readonly string settingsPath="...\\settings.json";// path to settings json in DL side
        private static readonly Dictionary<string, dynamic> data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(File.ReadAllText(settingsPath));
        public static dynamic get_string_value(string key){
            return data[key].GetString();
        }
        public static dynamic get_int_value(string key){
            return data[key].GetInt32();
        }
        public static dynamic get_double_value(string key){
            return data[key].GetDouble();
        }
        public static dynamic get_bool_value(string key){
            return data[key].GetBoolean();
        }
        public static dynamic get_loadout(){
            List<Tuple<int,int>> list = new List<Tuple<int,int>>();
            foreach (var item in data["loadout"].EnumerateArray()){
                var enumerator = item.EnumerateArray();
                enumerator.MoveNext();
                var first = enumerator.Current.GetInt32();
                enumerator.MoveNext();
                var second = enumerator.Current.GetInt32();
                list.Add(Tuple.Create(first, second));
            }
            return list;
        }
        public static void print_value(dynamic key){
            Console.WriteLine(data[key]);
        }
    }   
}