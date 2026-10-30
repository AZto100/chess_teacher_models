#include "chess.hpp"
#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <vector>
#include <chrono>
using namespace chess;
struct Limit{};
uint64_t nodes,cap;Color attacker;std::unordered_map<uint64_t,bool> tt;
bool mate(Board& b,int ply){
 if(++nodes>cap)throw Limit{};
 Movelist moves;movegen::legalmoves(moves,b);
 if(moves.empty())return b.inCheck()&&b.sideToMove()!=attacker;
 if(ply==0||b.halfMoveClock()>=100||b.isInsufficientMaterial()||b.isRepetition())return false;
 const auto key=b.hash()^(uint64_t(ply)*0x9e3779b97f4a7c15ULL)^(uint64_t(b.halfMoveClock())*0xd6e8feb86659fd93ULL);
 if(auto it=tt.find(key);it!=tt.end())return it->second;
 const bool ours=b.sideToMove()==attacker;
 std::vector<std::pair<int,Move>> ordered;
 for(auto m:moves){int score=0;if(ours)score=(b.givesCheck(m)!=CheckType::NO_CHECK?100:0)+(m.typeOf()==Move::PROMOTION?50:0)+(b.isCapture(m)?10:0);else score=b.isCapture(m)?20:0;ordered.emplace_back(score,m);}
 std::sort(ordered.begin(),ordered.end(),[](auto a,auto z){return a.first>z.first;});
 for(auto [score,m]:ordered){b.makeMove(m);bool result=mate(b,ply-1);b.unmakeMove(m);if(result==ours){if(tt.size()<2000000)tt[key]=ours;return ours;}}
 if(tt.size()<2000000)tt[key]=!ours;return !ours;
}
std::vector<Move> principal(Board& b,int ply){
 std::vector<Move> line;
 while(ply>0){
  Movelist ms;movegen::legalmoves(ms,b);if(ms.empty())break;
  bool ours=b.sideToMove()==attacker;std::vector<std::pair<int,Move>> order;
  for(auto m:ms)order.emplace_back(ours?((b.givesCheck(m)!=CheckType::NO_CHECK?100:0)+(m.typeOf()==Move::PROMOTION?50:0)+(b.isCapture(m)?10:0)):0,m);
  std::sort(order.begin(),order.end(),[](auto a,auto z){return a.first>z.first;});
  bool found=false;Move chosen;
  for(auto [score,m]:order){b.makeMove(m);bool good=ours?mate(b,ply-1):(ply<=2||!mate(b,ply-3));b.unmakeMove(m);if(good){chosen=m;found=true;break;}}
  if(!found)throw Limit{};
  line.push_back(chosen);b.makeMove(chosen);--ply;
 }
 return line;
}
int main(){std::string fen;int expected;uint64_t budget;
 while(std::cin>>expected>>budget){std::cin.ignore();std::getline(std::cin,fen);nodes=0;cap=budget;tt.clear();tt.reserve(500000);Board b(fen);attacker=b.sideToMove();
 try{bool lower=expected>1?mate(b,2*(expected-1)-1):false;bool yes=lower?true:mate(b,2*expected-1);std::vector<Move> line;if(yes&&!lower)line=principal(b,2*expected-1);std::cout<<(lower?"SHORTER":yes?"EXACT":"NO_MATE")<<" "<<nodes;if(!line.empty()){std::cout<<" PV";for(auto m:line)std::cout<<" "<<uci::moveToUci(m);}std::cout<<"\n";}
 catch(Limit&){std::cout<<"UNKNOWN "<<nodes<<"\n";}
 std::cout.flush();}
}
