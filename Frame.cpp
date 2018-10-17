/*
 * Frame.cpp
 *
 *  Created on: May 1, 2016
 *      Author: cchen
 */

#include "Frame.h"

#include<vector>
#include<set>
#include<sstream>
#include<fstream>
#include<iostream>
#include<stdexcept>

#include "../structs/AccountEntryStruct.h"
#include "../structs/FactorLoadingStruct.h"
#include "../structs/InfrastructureEntryStruct.h"
#include "../structs/PositionEntryStruct.h"
#include "../structs/SymbolStaticDataStruct.h"
#include "../structs/MarketDataTouchStruct.h"
#include "../structs/PretradeDataSummaryStruct.h"
#include "../structs/FeatureExtractorSummaryStruct.h"
#include "../structs/actionBookFeaturesExtractorConfigStruct.h"
#include "../structs/ContinuousBookFeaturesExtractorConfigStruct.h"
#include "../structs/IndexFeaturesExtractorConfigStruct.h"

#include <boost/lexical_cast.hpp>
#include "boost/format.hpp"
#include "TerranEnums.h"
#include <boost/tokenizer.hpp>
#include <boost/foreach.hpp>


using namespace zerg;

template<typename T>
Frame<T>::Frame(const std::string &filename) {

}

template<typename T>
Frame<T>::~Frame() {
    // TODO Auto-generated destructor stub
}

template
class Frame<AccountEntryStruct>;

template
class Frame<FactorLoadingStruct>;

template
class Frame<InfrastructureEntryStruct>;

template
class Frame<PositionEntryStruct>;

template
class Frame<SymbolStaticDataStruct>;

template
class Frame<MarketDataTouchStruct>;

template
class Frame<PretradeDataSummaryStruct>;

template
class Frame<FeatureExtractorSummaryStruct>;

template
class Frame<IndexFeaturesExtractorConfigStruct>;

template
class Frame<actionBookFeaturesExtractorConfigStruct>;

template
class Frame<ContinuousBookFeaturesExtractorConfigStruct>;
