const fs=require('fs');
const path=require('path'),vm=require('vm');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'x-player.html'),'utf8');
let embedded=html.slice(html.indexOf('var Chess960Rules'),html.indexOf('const PIECE_ARTWORK'));
embedded=embedded.replace('return __toCommonJS(adapter_exports);','return { ...__toCommonJS(adapter_exports), Chess, parseFen, makeFen, makeSquare };');
const sandbox={};vm.runInNewContext(embedded+';globalThis.rules=Chess960Rules;',sandbox);
const {Chess,parseFen,makeFen,makeSquare}=sandbox.rules;
const rows=[];for(let n=1;n<=6;n++)rows.push(...JSON.parse(fs.readFileSync(path.join(root,'puzzles','mate-'+n+'.json'),'utf8')).puzzles);
const uci=m=>makeSquare(m.from)+makeSquare(m.to)+(m.promotion?({queen:'q',rook:'r',bishop:'b',knight:'n'})[m.promotion]:'');
function gen(p){const out=[],ctx=p.ctx();for(const [from,ds]of p.allDests(ctx))for(const to of ds){if(p.board.getRole(from)==='pawn'&&(to<8||to>=56))for(const promotion of ['queen','knight','rook','bishop'])out.push({from,to,promotion});else out.push({from,to});}return out;}
function verify(row,ms){
 const p=Chess.fromSetup(parseFen(row.fen).unwrap()).unwrap(),attacker=p.turn;
 let nodes=0,tt=new Map(),choices=new Map(),deadline=Date.now()+ms;
 function search(p,d){
  if((++nodes&1023)===0&&Date.now()>deadline)throw Error('budget');
  const ctx=p.ctx(),moves=gen(p);
  if(!moves.length)return ctx.checkers.nonEmpty()&&p.turn!==attacker;
  if(d<=0||p.halfmoves>=100)return false;
  const k=makeFen(p.toSetup(),{epd:true})+'|'+d;if(tt.has(k))return tt.get(k);
  const atk=p.turn===attacker;
  const children=moves.map(m=>{const q=p.clone();q.play(m);return {q,m,check:q.isCheck()};});
  if(atk)children.sort((a,b)=>Number(b.check)-Number(a.check));
  if(atk&&d===1){for(const {q,check,m}of children)if(check&&q.isCheckmate()){tt.set(k,true);choices.set(k,m);return true;}tt.set(k,false);return false;}
  for(const {q,m}of children){const v=search(q,d-1);if(v===atk){tt.set(k,atk);if(atk)choices.set(k,m);return atk;}}
  tt.set(k,!atk);return !atk;
 }
 const result={id:row.id,legal:true};
 try{
  const first=gen(p).find(m=>uci(m)===row.firstMove);if(!first)throw Error('illegal source key');
  const q=p.clone();q.play(first);result.forcedWithin=search(q,row.mate*2-2);result.proofNodes=nodes;
  if(result.forcedWithin){
   let cur=p.clone(),d=row.mate*2-1,line=[];
   while(d>0&&!cur.isCheckmate()){
    const ms=gen(cur);let move;
    if(!line.length)move=first;
    else if(cur.turn===attacker){move=choices.get(makeFen(cur.toSetup(),{epd:true})+'|'+d)||ms.find(m=>{const q=cur.clone();q.play(m);return search(q,d-1);});}
    else move=ms[0];
    if(!move)break;line.push(uci(move));cur.play(move);d--;
   }
   result.line=line;result.endsInMate=cur.isCheckmate();
   const shorter=search(p,row.mate*2-3);result.exactMate=!shorter;result.shorterExists=shorter;
  }
 }catch(e){result.incomplete=e.message;}
 result.nodes=nodes;return result;
}
const selected=process.argv[2]?rows.filter(r=>r.id===process.argv[2]):rows;
if(!selected.length)throw new Error('Unknown puzzle ID');
for(const row of selected){const result=verify(row,Number(process.argv[3])||120000);console.log(JSON.stringify(result));if(!result.exactMate||!result.forcedWithin)process.exitCode=1;}
