/*
 * Frame.h
 *

 */

#ifndef CONFIGFRAME_H_
#define CONFIGFRAME_H_

#include<map>
#include<string>
#include<vector>

namespace ProjectNamespace {

    /**
     *  very light-weight container
     */
    template<typename T>
        class Frame {
            size_t _columnNum = 0;
            std::vector<std::string> _columnNames;

            public:
            std::vector<T> entries;

            public:

            Frame(const std::string &filename){


                std::cout << "loading config frame " << filename << std::endl;

                boost::char_separator<char> sep(",");

                std::ifstream infile(filename.c_str());

                if (!infile) {
                    std::cout << filename;
                    throw std::runtime_error("[ERROR] the frame filename does not exist!");
                }

                std::string line;

                std::getline(infile, line);

                boost::tokenizer<boost::char_separator<char> > tokens1(line, sep);

                for (const std::string &s : tokens1) {
                    _columnNames.push_back(s);
                    _columnNum++;
                }

                for (size_t c = 0; c < _columnNum; ++c) {
                    std::cout << "Frame " << c << "->" << _columnNames[c] << std::endl;
                }

                int i = 0;

                while (std::getline(infile, line)) {
                    if (line.size() <= 1)
                        continue;

                    boost::tokenizer<boost::char_separator<char> > tokens(line, sep);

                    T entry(_columnNames, tokens);

                    entries.push_back(entry);

                    ++i;
                }

                std::cout << "Frame::Frame loaded  " << entries.size() << "entries from " << filename << std::endl;
            }

            inline size_t size(){return entries.size();}

            virtual ~Frame();
        };

} /* namespace  */

#endif /* CONFIGFRAME_H_ */
