"""loader and boilerplate scripts for the application"""

from typing import Literal
from types import NoneType
from sys import maxsize as _sys_max_int
from re import search as _regex_search
from math import inf as _inf
from datetime import datetime
from os import makedirs
from os.path import \
    sep,\
    exists,\
    isdir,\
    isfile,\
    realpath

class Lib:
    """Stores the core boiler-plate functions needed for the application to run"""
    class Gui:
        """Controls the graphical user interface that the end-user is intended to interect with to control the application"""
    class Logger:
        """Event logger for the application in-case of crashes or need of filing bug reports to replicate end-user's taken actions within the application"""
        class Default:
            """Default values for the event logger"""
            level:dict={"value":20,"alias":"Info"}
            encoding:str="utf-8"
            output_path:str="./users/logs"
            allowed_levels= ["Debug","Info","Warning","Error","Critical"]
    
        @classmethod
        def normalize_level(cls, new_level:str|int)-> dict:
            """
            Parse a given level to recieve a normalized output
            
            ---

            Use this as a default for sterilizing inputs elsewhere
            """

            #region Sterilize input
            if not isinstance(new_level,(str,int,float)):# Detect invalid input type
                raise TypeError(f"new_level must be of type string, int or float not {type(new_level)}")
            new_level= int(new_level) if not isinstance(new_level, (int,str)) else new_level
            new_level= str(new_level).strip().lower() if not isinstance(new_level, str) else new_level.strip().lower()
            
            if new_level=="":
                raise ValueError("new_level must not be a blank string. Please double check your inputs")
            #endregion Sterilize input

            match new_level:# to assign a value if expected value is found
                case "1"|"10"|"debug":
                    return {"value":10,"alias":"Debug"}
                case "2"|"20"|"info"|"information":
                    return {"value":20,"alias":"Info"}
                case "3"|"30"|"warn"|"warning":
                    return {"value":30,"alias":"Warning"}
                case "4"|"40"|"err"|"error":
                    return {"value":40,"alias":"Error"}
                case "5"|"50"|"crit"|"critical":
                    return {"value":50,"alias":"Critical"}
                case _:
                    # No valid match found
                    try:# to convert to integer and find range value fits within FIRST and assign value
                        new_level=int(new_level)
                        if new_level<20:
                            return {"value":10,"alias":"Debug"}
                        elif new_level<30:
                            return {"value":20,"alias":"Info"}
                        elif new_level<40:
                            return {"value":30,"alias":"Warning"}
                        elif new_level<50:
                            return {"value":40,"alias":"Error"}
                        elif new_level>50:
                            return {"value":50,"alias":"Critical"}
                    except ValueError:# due to not being able to convert datatype, so default value instead
                        return Lib.Logger.Default.level

        # Current class called
        def __init__(self, output_path:str="./user/logs", /,
                    encoding:str="utf-8", 
                    handler:Literal["log","print"]="log",
                    level:Literal[10,"Debug",20,"Info",30,"Warning",40,"Error",50,"Critical"]="Info")-> NoneType:
            self.__level=self.normalize_level(new_level=level)
            #region WIP
            self.__output_path= output_path
            self.__handler=self.__pick_handler(handler)
            self.__encoding=self.__check_encoding(encoding)
            #endregion WIP

            print(
                f"Current logging level == {self.level['alias']}",
                f"Current logging handler == {self.__handler}",
                f"Current logging encoding == {self.__encoding}",
                sep="\n"
                )
            if not self.__handler=="console":
                print(f"Current logging output == {self.__output_path}",)
        
        #region Current logging level
        @property
        def level(self)-> dict:
            return self.__level
        @level.getter
        def level(self)-> dict:
            return self.__level
        @level.setter
        def level(self, new_level:Literal[10,"Debug",20,"Info",30,"Warning",40,"Error",50,"Critical"])-> None:
            self.__level=self.normalize_level(new_level)
            print(f"Set current logging level to {self.__level}")
        #endregion Current logging level
        #region Current output path
        @property
        def output_path(self)-> str:
            return self.__output_path
        @output_path.getter
        def output_path(self)-> str:
            return self.__output_path
        @output_path.setter
        def output_path(self, new_path)-> None:
            self.__output=Lib.System_Info.Path.validate(new_path) if not Lib.System_Info.Path.validate(new_path, return_exists=False, return_isfile=False, return_isdir=False, return_new_path=True)[0] is None else Lib.Logger.Default.output_path
        #endregion Current output path
        #region WIP
        def __check_encoding(self, value:str, /)-> str:
            return value
        def __pick_handler(self, output_handler:Literal["console","file"]="file")->str:
            return "console" if output_handler=="console" and self.level.lower()=="debug" else "file"
        #endregion WIP
    class Mathapedia:
        """
        Math as taught in school if taught in step to an elementary schooler
        
        This is as many computational forms of math that I (St0rm) could work out by myself from reading online formulas as well as remember from school.
        The point of this module albiet slower than the native C-based counterpart already implemented is to retain higher precision with longer values.

        If an answer exceeds precision point, value will be compressed for memory reasons.
        If value would result in an infinite number (calculates further than retained precision), value is compressed to the precision point and suffixed with "e+/-\u221E"
        """
        vinculum_unicode_str:str= u"\u0305" # used to notate repeating decimal value
        lemniscate_unicode_str:str= u"\u221E" # Infinity symbol

        def infinity(value:str|int|float):
            """
            Represents forms of infinity
            
            Defaults to try and use your system's max value as a stand-in for infinity

            Should your value be higher than your systems max size value, math.inf is substituted
            """

            match value:
                case str():
                    value= value.replace("\u0020"," ").replace(" ","")

                    #region validate str as numberical format syntax
                    invalid_entry_format_err:str= "Input is not a valid number! Please check that value, has been handled properly before parsing again."
                    if _regex_search("[^0-9.-]",value) is not None:
                        raise ValueError(invalid_entry_format_err)
                    elif value.count(".")>1:
                        raise ValueError(invalid_entry_format_err)
                    elif value.count("-")!=0 and not value.startswith("-") or value.count("-")>1:
                        raise ValueError(invalid_entry_format_err)
                    #endregion validate str as numberical format syntax

                    return _inf if int(value)>=_sys_max_int else _sys_max_int
                case int():
                    return _inf if value>=_sys_max_int else _sys_max_int
                case float():
                    if str(value)==str(float('nan')):
                        return _sys_max_int
                    return _inf if value>=_sys_max_int else _sys_max_int
                case _:
                    raise TypeError(f"value must be of type str | int | float not {type(value)}")
        def isNegative(value:str|int|float)-> bool:
            """Returns if value is a nagative value"""
            value= float(value) if not isinstance(value,float) else value
            return True if value<0 else False

        #region PEMDAS
        def parenthesis(*args,**kwargs)-> str:
            return
        def exponents(value,base:int|float=10,power:int=1)-> str:
            return
        def multiply(value_a:str|int|float=0,value_b:str|int|float=0, retain_precision:str|int|float="∞")-> str:
            return
        def divide(value_a:str|int|float=0,value_b:str|int|float=0, retain_precision:str|int|float="∞")-> str:
            return
        def add(value_a:str|int|float=0,value_b:str|int|float=0, retain_precision:str|int|float="∞")->str:
            """Sums two values and returns a stringed-floating point value
            
            :retain_precision: Max number of floating point placements allowed to be retained

            ---

            i.e. retain_precision=0 results in an integer value shown as a string

            retain_precision>=1 results in a floating point value with placements allowed up to specified amount

            NOTE: Excess values will result in a flooring to save memory

            Repeating values will use a vinculum notation (i.e. ̅3̅3)
            """

            #region sterilize input
            #region input not right type
            if not isinstance(value_a,(str,int,float)):
                raise TypeError(f"Please ensure value_a is of type str, int or float not {type(value_a)}")
            elif not isinstance(value_b,(str,int,float)):
                raise TypeError(f"Please ensure value_b is of type str, int or float not {type(value_b)}")
            elif not isinstance(retain_precision,(str,int,float)):
                raise TypeError(f"Please ensure retain_precision is of type str, int or float not {type(retain_precision)}")
            #endregion input not right type
            #region format incomming input
            value_a= str(value_a) if not isinstance(value_a,str) else value_a.strip()
            value_b= str(value_b) if not isinstance(value_b,str) else value_b.strip()

            if value_a.startswith("."):
                value_a=f"0{value_a}"
            elif value_a.startswith("-."):
                value_a=f"-0.{value_a[2:]}"
            elif value_a.startswith("+."):
                value_a=f"0.{value_a[2:]}"
            elif value_a.startswith("+"):
                value_a=f"{value_a[1:]}"
            
            if value_b.startswith("."):
                value_b=f"0{value_b}"
            elif value_b.startswith("-."):
                value_b=f"-0.{value_b[2:]}"
            
            if value_a.count(".")==0:
                value_a= f"{value_a}.0"
            if value_b.count(".")==0:
                value_b= f"{value_b}.0"
            
            match retain_precision:
                case str(float("inf")):
                    retain_precision=_sys_max_int
                case str(float("-inf")):
                    retain_precision=1
                case float()|str():
                    if isinstance(retain_precision,float):
                        retain_precision=int(retain_precision)
                    elif retain_precision.strip()==Lib.Mathapedia.lemniscate_unicode_str:
                        retain_precision=_sys_max_int
            if retain_precision<1:
                retain_precision=1
            #endregion format incomming input

            #region Nothing added
            if float(value_a)==0.0:
                return value_b
            elif float(value_b)==0.0:
                return value_a
            #endregion nothing added
            
            #region store if value is negative
            value_a_isnegative= Lib.Mathapedia.isNegative(value_a)
            value_b_isnegative= Lib.Mathapedia.isNegative(value_b)
            #endregion store if value is negative

            value_a=value_a[1:] if value_a.startswith(("+","-")) else value_a
            value_b=value_b[1:] if value_b.startswith(("+","-")) else value_b

            retain_precision=1 if retain_precision<=1 else retain_precision
            #endregion sterilize input

            #Value_A is now in float format as a string
                # Checked if negative
            #Value_B is now in float format as a string
                # Checked if negative
            #Retain_Precision is now within range(1-infinity)

            #region split value into int and float
            value_a_int= value_a.rsplit(".",1)[0]
            value_a_float= value_a.rsplit(".",1)[1]

            value_b_int= value_b.rsplit(".",1)[0]
            value_b_float= value_b.rsplit(".",1)[1]
            #endregion split value into int and float

            #region format split values
            #region format ints to matching lengths
            if len(value_a_int)<len(value_b_int):# int b longer than int a
                float_len_offset= len(value_b_int)-len(value_a_int)
                value_a_int= f"{'0'*float_len_offset}{value_a_int}"
            elif len(value_b_int)<len(value_a_int):# int a longer than int b
                float_len_offset= len(value_a_int)-len(value_b_int)
                value_b_int= f"{'0'*float_len_offset}{value_b_int}"
            #endregion format ints to matching lengths
            #region format floats to matching lengths
            if len(value_a_float)<len(value_b_float):# float b longer than float a
                float_len_offset= len(value_b_float)-len(value_a_float)
                value_a_float= f"{value_a_float}{'0'*float_len_offset}"
            elif len(value_b_float)<len(value_a_float):# float a longer than float b
                float_len_offset= len(value_a_float)-len(value_b_float)
                value_b_float= f"{value_b_float}{'0'*float_len_offset}"
            #endregion format floats to matching lengths
            #endregion format split values

            #region check which combination is negative
            both_values_query_negative:set[bool]={value_a_isnegative is True, value_b_isnegative is True}
            #region use subtraction if sum is not both positive or negative
            if any(both_values_query_negative) and not all(both_values_query_negative):
                if abs(float(value_a))==abs(float(value_b)):# +-(x) == 0
                    return f'0'
                
                elif abs(float(value_a))<abs(float(value_b)):# Answer will be positive
                    # reverse operation if value_a  is negative
                    # this means make sure the positive value is equated first
                    highest_value= f"{value_a_int}.{value_a_float}" if not value_a_isnegative else f"{value_b_int}.{value_b_float}"
                    lowest_value= f"-{value_a_int}.{value_a_float}" if value_a_isnegative else f"-{value_b_int}.{value_b_float}"
                    full_answer= Lib.Mathapedia.subtract(highest_value, lowest_value[1:])
                    
                    print(
                        highest_value,
                        lowest_value,
                        '='*len(f'-{value_a_int}.{value_a_float}'),
                        full_answer,
                        sep="\n"
                        )
                elif abs(float(value_a))>abs(float(value_b)):# answer will be negative
                    full_answer="0" # WIP
            #endregion use subtraction if sum is not both positive or negative
            #region both sums are negative or both positive
            else:
                zipped_ints:list[zip]=list(zip(value_a_int[::-1], value_b_int[::-1]))
                zipped_floats:list[zip]=list(zip(value_a_float[::-1], value_b_float[::-1]))

                carry_value:int=0

                #region sum both floats
                neg_float_summed_values:list=[]
                for index in zipped_floats:
                    a_float,b_float=index            
                    summed_val= int(a_float)+int(b_float)+carry_value

                    if summed_val>=10:
                        carry_value=1
                        remainder=summed_val-10

                        neg_float_summed_values.append(str(remainder))
                        continue
                    neg_float_summed_values.append(str(summed_val))
                    carry_value=0

                #endregion sum both floats
                #region sum both integers
                neg_int_summed_values:list=[]

                for index in zipped_ints:
                    a_int,b_int=index            
                    summed_val= int(a_int)+int(b_int)+carry_value

                    if summed_val>=10:
                        carry_value=1
                        remainder=summed_val-10
                        neg_int_summed_values.append(str(remainder))
                        continue

                    neg_int_summed_values.append(str(summed_val))
                    carry_value=0

                if carry_value>0:
                    neg_int_summed_values.append(str(carry_value))
                    carry_value=0

            #endregion sum both integers
                full_answer= f"{'-' if all(both_values_query_negative) is True else ''}{''.join(neg_int_summed_values[::-1]).lstrip('0') if ''.join(neg_int_summed_values[::-1]).lstrip('0')!='' else '0'}.{''.join(neg_float_summed_values[::-1]).rstrip('0')}"
            #endregion both sums are negative or both positive
            #endregion check which combination is negative
            return full_answer[:retain_precision] if float(full_answer)>retain_precision else full_answer
        def subtract(value_a:str|int|float=0,value_b:str|int|float=0, retain_precision:str|int|float="∞")-> str:
            """Subtracts 2 values with varying precision"""
            #region sterilize input
            #region input not right type
            if not isinstance(value_a,(str,int,float)):
                raise TypeError(f"Please ensure value_a is of type str, int or float not {type(value_a)}")
            elif not isinstance(value_b,(str,int,float)):
                raise TypeError(f"Please ensure value_b is of type str, int or float not {type(value_b)}")
            elif not isinstance(retain_precision,(str,int,float)):
                raise TypeError(f"Please ensure retain_precision is of type str, int or float not {type(retain_precision)}")
            #endregion input not right type
            #region format incomming input
            value_a= str(value_a) if not isinstance(value_a,str) else value_a.strip()
            value_b= str(value_b) if not isinstance(value_b,str) else value_b.strip()

            if value_a.startswith("."):
                value_a=f"0{value_a}"
            elif value_a.startswith("-."):
                value_a=f"-0.{value_a[2:]}"
            elif value_a.startswith("+."):
                value_a=f"0.{value_a[2:]}"
            elif value_a.startswith("+"):
                value_a=f"{value_a[1:]}"
            
            if value_b.startswith("."):
                value_b=f"0{value_b}"
            elif value_b.startswith("-."):
                value_b=f"-0.{value_b[2:]}"
            
            if value_a.count(".")==0:
                value_a= f"{value_a}.0"
            if value_b.count(".")==0:
                value_b= f"{value_b}.0"
            
            match retain_precision:
                case str(float("inf")):
                    retain_precision=_sys_max_int
                case str(float("-inf")):
                    retain_precision=1
                case float()|str():
                    if isinstance(retain_precision,float):
                        retain_precision=int(retain_precision)
                    elif retain_precision.strip()==Lib.Mathapedia.lemniscate_unicode_str:
                        retain_precision=_sys_max_int
            if retain_precision<1:
                retain_precision=1
            #endregion format incomming input

            #region Nothing subtracted
            if float(value_a)==0.0:
                return value_b
            elif float(value_b)==0.0:
                return value_a
            #endregion nothing subtracted
            
            #region store if value is negative
            value_a_isnegative= Lib.Mathapedia.isNegative(value_a)
            value_b_isnegative= Lib.Mathapedia.isNegative(value_b)
            #endregion store if value is negative

            value_a=value_a[1:] if value_a.startswith(("+","-")) else value_a
            value_b=value_b[1:] if value_b.startswith(("+","-")) else value_b

            retain_precision=1 if retain_precision<=1 else retain_precision
            #endregion sterilize input

            #Value_A is now in float format as a string
                # Checked if negative
            #Value_B is now in float format as a string
                # Checked if negative
            #Retain_Precision is now within range(1-infinity)
            print(f"subtract({value_a},{value_b})")
            zipped_values:list[zip]= list(enumerate(zip(value_a[::-1], value_b[::-1])))
            both_values_query_negative:set[bool]= {value_a_isnegative is True, value_b_isnegative is True}

            print(f"Index{' '*(len(zipped_values)-len('index'))}| Paired Values")
            print(f"{'-'*len('index')}{'-'*(len(zipped_values)-len('index'))}|{'-'*len(' Paired Values')}")
            if not any(both_values_query_negative):# Both inputs are positive

                if float(value_a)<float(value_b):# answer will be negative
                    pass
                else:# answer will be positive
                    pass
            return
        #endregion PEMDAS

        def factorial(value):
            yield
        def factors():
            yield
        def multiples():
            yield

        def average(*args):
            return
        def median(*args):
            return
        def outlier(*args):
            return

        def logarithm():
            return
        def tangent():
            return
        def sine():
            return
        def cosine():
            return
        def pythagorian_theorem():
            return

        def length():
            return
        def perimeter(dimsions:zip):
            return
        def surface_area():
            return
        def circumference(radius:int|float=None,diameter:int|float=None):
            return
        def area(dimensions:zip):
            return
        def volume(dimensions:zip):
            return

        def quadratics():
            return
        def probability():
            return
        def percentage():
            return

        def distance():
            return
        def midpoint():
            return
        def speed():
            return
        def velocity():
            return
        def pressure():
            return
        def temp(value:int|float=0,standard='c')->str:
            return
        def timezone():
            return
        def timestamp():
            return
        def time():
            return

        def slope():
            return
        def slope_intercept():
            return
        def sys_of_linear_eq():
            return

        def equality():
            return
        def inequality():
            return

        def matrix():
            return

    class Sanitation:
        """Sterilizes ALL inputs potentially varied by actions of an end-user to minimize security issues and crashes due to improper data handling"""
    class Settings:
        """
        Controls the application's internal settings,
        using a data base type-locked dictionary comparison of the factory settings as defaults and end-user settings are primary where permitted
        """
    class System_Info:
        """
        Reports information autonomously generated by the computer, this is for proper logging actions as well as other forms of handling
        
        This has highest risk of exposing a user's personal files or information, treat carefully if adding new functionality here
        """
        class Runtime:
            def __sort_argkwarg()-> dict:
                from sys import argv as __argv
                argumentative_kwargs=frozenset(__argv)
                kwargs:dict={}
                args:list=[]
                for arg_or_kwarg in argumentative_kwargs:
                    arg_or_kwarg=arg_or_kwarg.strip()
                    if "=" in arg_or_kwarg:
                        kw,arg=arg_or_kwarg.split("=",1)
                        kw=kw.strip()
                        arg=arg.strip() if not arg.strip()=="" else "None"

                        kwargs[kw]=arg
                    else:
                        match arg_or_kwarg:
                            case ""|"-m":# empty string or package flag
                                continue
                        args.append(arg_or_kwarg)
                
                # Check paired flags are not present in both searches
                for kwarg in kwargs.copy():
                    match kwarg.lower():
                        case "--debug":
                            if "-d" in args:
                                kwargs.pop(kwarg)
                                continue
                        case "--test-suite":
                            if "-ts" in args:
                                kwargs.pop(kwarg)
                
                args=frozenset(args)
                return {"args":args,"kwargs":kwargs}
            args=__sort_argkwarg().get("args",None).copy()
            kwargs=__sort_argkwarg().get("kwargs",None).copy()

                                # Branch.Sub-Branch.NamedFork.Rewrite.MajorUpdate.SecurityUpdate.BugFix.Patch.Snapshot
            version:str="dev.sandbox.St0rmWalker.pkg_template.0.0.0.0.0.00000001"

        class Path:
            def validate(output_path:str, /, return_exists:bool=True, return_isfile:bool=True, return_isdir:bool=True, return_new_path:bool=True)->list|None:
                    """
                    Returning "False" for return_new_path will result in no creation of directory if does not already exist
                    """
                    answer=[]
                    
                    default_path= fr'{realpath("../..").replace("/",sep).replace(f"{sep}{sep}",sep)}{sep}'
                    output_path= fr'{output_path.replace("/",sep).replace(f"{sep}{sep}",sep)}' if sep in output_path or "/" in output_path else default_path
                    
                    expected_path_type= "file" if "." in output_path.rsplit(sep,1)[1] else "dir"
                    
                    path_exists= True if exists(output_path) else False
                    path_isfile= True if isfile(output_path) else False
                    path_isdir= True if isdir(output_path) else False
                    path_isdefault= True if output_path==default_path else False

                    if not path_isdefault:# Check if path exists and how
                        if path_exists is True:
                            if return_exists is True:
                                answer.append(path_exists)
                            if return_isfile is True:
                                answer.append(path_isfile)
                            if return_isdir is True:
                                answer.append(path_isdir)
                        else:
                            match expected_path_type:
                                case "file":# generate new file at location
                                    if return_new_path is True:
                                        with open(output_path,"w"): pass
                                    if return_exists is True:
                                        answer.append(True)
                                    if return_isfile is True:
                                        answer.append(True)
                                    if return_isdir is True:
                                        answer.append(False)
                                case "dir":# generate a new directory at location
                                    if return_new_path is True:
                                        makedirs(output_path, exist_ok=True)
                                    if return_exists is True:
                                        answer.append(True)
                                    if return_isfile is True:
                                        answer.append(True)
                                    if return_isdir is True:
                                        answer.append(False)
                    else:# Path exists with some default values already known
                        if return_exists is True:
                            answer.append(True)
                        if return_isfile is True:
                            answer.append(True if isfile(default_path) else False)
                        if return_isdir is True:
                            answer.append(True)
                    
                    if return_new_path is True:# insert current valid path and create it if not already exists
                        answer.insert(0,fr"{output_path}")

                    return answer if answer!=[] else None

        class Time:
            """
            Uses a little mathematics and the datetime library to expand on some uses for this application that're frequently used
            
            For finest case control, using datetime directly is still recommended
            """
            @classmethod
            def timestamp(cls, /)-> float:
                return datetime.timestamp(datetime.now())
            @classmethod
            def read_timestamp(cls, snowflake:float, /, human_readable:bool=False, international:bool=False)-> str:
                year, month, day, hour, minute, second, millisecond= str(datetime.fromtimestamp(snowflake)).replace("-"," ").replace(":"," ").replace("."," ").split(" ",6)
                month, day, hour= int(month), int(day), int(hour)
                if human_readable is True:
                    #region value aliasing
                    month_alias={
                        1 :"January",
                        2 :"February",
                        3 :"March",
                        4 :"April",
                        5 :"May",
                        6 :"June",
                        7 :"July",
                        8 :"August",
                        9 :"September",
                        10:"October",
                        11:"November",
                        12:"December"
                    }
                    ending_pronounciation={
                        1:"first",
                        2:"second",
                        3:"third",
                        4:"fourth",
                        5:"fifth",
                        6:"sixth",
                        7:"seventh",
                        8:"eighth",
                        9:"nineth",
                        10:"tenth",
                        11:"eleventh",
                        12:"twelfth",
                        13:"thirteenth",
                        14:"fourteenth",
                        15:"fifteenth",
                        16:"sixteenth",
                        17:"seventeenth",
                        18:"eighteenth",
                        19:"nineteenth",
                        20:"twentieth",
                        30:"thirtieth",
                    }
                    #endregion value aliasing
                    # region associate day number with written form
                    if day<=20 or day==30:
                        day= ending_pronounciation[day]
                    elif 20<day<30:
                        day=f"twenty {ending_pronounciation[day-20]}"
                    else:
                        day="thirty first"
                    #endregion associate day number with written form
                    if international is True:
                        return f"{hour}:{minute}:{second}.{millisecond} on the {day} day of {month_alias[month]}, {year}"
                    return f"{hour-12 if hour>12 else hour}:{minute}:{second}.{millisecond} {'am' if hour<12 else 'pm'} on the {day} day of {month_alias[month]}, {year}"
                return str(datetime.fromtimestamp(snowflake)) if international is True else f"{month}-{day}-{year} {hour}:{minute}:{second}.{millisecond}"
            @classmethod
            def datetime_format(cls, /)-> str:
                return "HOUR(24/12):MINUTE:SECOND.MICROSECOND on the DAY(written) day of MONTH, YEAR"
            @classmethod
            def timestamp_offset(cls, /, snowflake_a:str, snowflake_b:str)-> str:
                return str(snowflake_a-snowflake_b) if snowflake_a>snowflake_b else f"-{snowflake_b-snowflake_a}"
            @classmethod
            def utc_offset(cls, /)-> str:
                utc_timenow=datetime.utcnow()
                lan_timenow=datetime.fromtimestamp(Lib.System_Info.Time.timestamp())

                return Lib.System_Info.Time.timestamp_offset(lan_timenow,utc_timenow)

    class Update:
        """Checks if new updates are available and handles the update if allowed to auto-update"""
