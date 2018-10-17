#ifndef AUTO_GEN_CSV_LOADER_H_
#define AUTO_GEN_CSV_LOADER_H_
#include <boost/lexical_cast.hpp>
#include <boost/tokenizer.hpp>
#include "../utilities/ProjectEnums.h"
#include "../utilities/ProjectTypes.h"
#include <boost/foreach.hpp>
#include <vector>
namespace terran {
class test {
public:
int32_t city =0;
int32_t holiday =0;
double happiness =0.0;
JobEnum job =static_cast<JobEnum>(0);
test()	{;}
test(std::vector<std::string> columnNames, boost::tokenizer< boost::char_separator<char> > tokens){
	size_t i = 0;
	for (const std::string& t : tokens) {
if (columnNames[i] == std::string("city")){city = boost::lexical_cast<int32_t>(t);}

if (columnNames[i] == std::string("holiday")){holiday = boost::lexical_cast<int32_t>(t);}

if (columnNames[i] == std::string("happiness")){happiness = boost::lexical_cast<double>(t);}

if (columnNames[i] == std::string("job")){job = EnumParser::fromStringJobEnum(t);}

++i;
}
}
virtual ~test(){};
bool operator < (const	test& o) const	{	return o.city < city;}
int32_t getKey () const	{	return city;}
};



}
#endif
