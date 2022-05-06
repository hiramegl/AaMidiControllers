require 'yaml';

hEffects = {
  'Vocoder'          => 3,
  'Overdrive'        => 1,
  'BeatRepeat'       => 2,
  'Compressor2'      => 2,
  'Resonator'        => 6,
  'AutoPan'          => 2,
  'Echo'             => 6,
  'Delay'            => 2,
  'FilterDelay'      => 4,
  'GrainDelay'       => 2,
  'Chorus'           => 2,
  'Flanger'          => 3,
  'Phaser'           => 3,
  'FrequencyShifter' => 2,
  'Reverb'           => 3,
  'Eq8'              => 2,
  'FilterEQ3'        => 1,
  'Redux'            => 1,
}

hFxBanks  = {}
nBank     = 0
nOffset   = 0

hEffects.each { |sEffect, nStrips|
  unless hFxBanks[nBank]
    hFxBanks[nBank] = {
      'Group' => {
        'Button' => {
          '0' => Array.new(8),
          '1' => Array.new(8),
          '2' => Array.new(8),
          '3' => Array.new(8),
        },
        'Rotary' => {
          '0' => Array.new(8),
          '1' => Array.new(8),
          '2' => Array.new(8),
          '3' => Array.new(8),
        }
      },
      'Main' => {
        'Button' => {
          '0' => Array.new(8),
          '1' => Array.new(8),
        },
        'Rotary' => {
          '0' => Array.new(8),
          '1' => Array.new(8),
          '2' => Array.new(8),
        }
      },
    }
  end
  puts("> #{sEffect} [#{nStrips}]")
  aConfig = File.readlines("#{sEffect}_config.txt")
  aConfig.each { |sLine|
    sLine = sLine.strip
    next if sLine[0] == '#';
    next if sLine == nil;
    next if sLine.length == 0;
    aParts = sLine.split('|');
    sParam = aParts[0].strip;
    sPos   = aParts[1].strip;
    sPos =~ /(\w+)_(\w+)_(\d)_(\d)/;
    sType  = $1;
    sCtrl  = $2;
    sRow   = $3;
    nStrip = Integer($4);
    sStyle = '';
    if (sParam == 'Device On')
      sStyle = ' device-on';
    elsif (sParam =~ /Dry.?Wet/)
      sStyle = ' dry-wet';
    end
    sParam = "#{sEffect}<br/>On/Off" if sParam == 'Device On';
    hFxBanks[nBank][sType][sCtrl][sRow][nOffset + nStrip] = "<td class='#{sEffect}#{sStyle}'>#{sParam}</td>"
  }

  nOffset += nStrips
  if nOffset >= 8
    nBank += 1
    nOffset = 0
  end
}
#puts(hFxBanks.to_yaml)

aInstruments = [
  'UltraAnalog',
  'Collision',
  'LoungeLizard',
  'Operator',
  'MultiSampler',
  'OriginalSimpler',
  'StringStudio',
  'InstrumentVector',
]

hInsBanks = {}
aInstruments.each { |sInstrument|
  puts("> #{sInstrument}")
  hInsBanks[sInstrument] = [] unless hInsBanks[sInstrument];
  aConfig = File.readlines("#{sInstrument}_config.txt")

  aConfig.each { |sLine|
    sLine = sLine.strip
    next if sLine[0] == '#';
    next if sLine == nil;
    next if sLine.length == 0;
    aParts = sLine.split('|')
    sParam = aParts[0].strip
    sPos   = aParts[1].strip
    sPos =~ /(\w+)_(\w+)_(\d)_(\d)_(\d)/
    sType  = $1
    sCtrl  = $2
    sRow   = $3
    nStrip = Integer($4)
    nBank  = Integer($5)

    unless hInsBanks[sInstrument][nBank]
      hInsBanks[sInstrument][nBank] = {
        'Group' => {
          'Button' => {
            '0' => Array.new(8),
            '1' => Array.new(8),
            '2' => Array.new(8),
            '3' => Array.new(8),
          },
          'Rotary' => {
            '0' => Array.new(8),
            '1' => Array.new(8),
            '2' => Array.new(8),
            '3' => Array.new(8),
          }
        },
        'Main' => {
          'Button' => {
            '0' => Array.new(8),
            '1' => Array.new(8),
          },
          'Rotary' => {
            '0' => Array.new(8),
            '1' => Array.new(8),
            '2' => Array.new(8),
          }
        },
      }
    end
    sStyle = '';
    if (sParam == 'Device On')
      sStyle = ' device-on';
    end
    sParam = "#{sInstrument}<br/>#{sParam}" if sParam == 'Device On';

    hInsBanks[sInstrument][nBank][sType][sCtrl][sRow][nStrip] = "<td class='#{sInstrument}#{sStyle}'>#{sParam}</td>"
  }
}
#puts(hInsBanks.to_yaml)

sScript = <<__FUN__
function on_group(_nGroup) {
  for (var i = 0; i < 9; i++) {
    var oEl = document.getElementById('group-' + i)
    oEl.style.display = (i == _nGroup) ? 'block' : 'none';
  }
}
function on_bank(_nGroup, _nBank) {
  for (var i = 0; i < 6; i++) {
    var oEl = document.getElementById('bank-' + _nGroup + '-' + i)
    if (oEl == null) continue;
    oEl.style.display = (i == _nBank) ? 'block' : 'none';
  }
}
__FUN__

aHtml = ['<head>'];
aHtml << '<style>';
aHtml << 'body {font-family: monospace; font-size: 12px}';
aHtml << 'table {border-spacing: 0px}';
aHtml << 'td {border: solid 1px; width: 200px; height: 48px; font-size: 18px; text-align: center;}';
aHtml << 'button {margin: 2px; padding: 1px 20px; height: 40px; font-weight: bold;}';
#aHtml << 'button {margin: 2px; padding: 1px 20px; background-color: black; color: white; height: 40px; font-weight: bold;}';
aHtml << '.Group-header     {background-color: #666666; color: white; font-weight: bold;}';
aHtml << '.Main-header      {background-color: #000000; color: white; font-weight: bold;}';
aHtml << '.device-on        {background-color: #333333 !important; color: white !important; font-weight: bold;}';
aHtml << '.dry-wet          {background-color: #729fcf !important; color: black !important; font-weight: bold;}';
aHtml << '.Vocoder          {background-color: #ff99ff}';
aHtml << '.Overdrive        {background-color: #cc66ff}';
aHtml << '.BeatRepeat       {background-color: #ff9999}';
aHtml << '.Compressor2      {background-color: #ff66cc}';
aHtml << '.Resonator        {background-color: #ffcc00}';
aHtml << '.AutoPan          {background-color: #ff6600}';
aHtml << '.Echo             {background-color: #66ff00}';
aHtml << '.Delay            {background-color: #66cc00}';
aHtml << '.FilterDelay      {background-color: #00cc33}';
aHtml << '.GrainDelay       {background-color: #006600; color: white;}';
aHtml << '.Chorus           {background-color: #9999ff}';
aHtml << '.Flanger          {background-color: #3399ff}';
aHtml << '.Phaser           {background-color: #009999}';
aHtml << '.FrequencyShifter {background-color: #00ffff}';
aHtml << '.Reverb           {background-color: #ff9999}';
aHtml << '.Eq8              {background-color: #ff0000}';
aHtml << '.FilterEQ3        {background-color: #cc0000; color: white;}';
aHtml << '.Redux            {background-color: #cc3300}';
aHtml << '.Effects          {background-color: #000000; color: white;}';
aHtml << '.UltraAnalog      {background-color: #ffcc00}';
aHtml << '.Collision        {background-color: #ff9999}';
aHtml << '.LoungeLizard     {background-color: #ccccff}';
aHtml << '.Operator         {background-color: #3399ff}';
aHtml << '.MultiSampler     {background-color: #33ff33}';
aHtml << '.OriginalSimpler  {background-color: #00cc33}';
aHtml << '.StringStudio     {background-color: #33cccc}';
aHtml << '.InstrumentVector {background-color: #cc99ff}';
aHtml << '</style>';
aHtml << '<script type="text/javascript">';
aHtml << sScript;
aHtml << '</script>';
aHtml << '</head>';
aHtml << '<body>';

# BANK GROUP BUTTONS *********************************************************************
aMenu = ["<button class='Effects' onclick='on_group(0)'>EFFECTS</button>"];
aInst = %w(Analog Collision Electric Operator Sampler Simpler Tension Wave)
aClss = hInsBanks.keys;
aMenu << Range.new(0, aInst.length - 1).collect { |nIdx|
  "<button class='#{aClss[nIdx]}' onclick='on_group(#{nIdx + 1})'>#{aInst[nIdx].upcase}</button>"
}.join("\n")
aHtml << aMenu;
aHtml << "<br/>";

# EFFECTS GROUP BUTTONS ******************************************************************
aHtml << "<div id='group-0' style='display: block'>";
sBanks = hFxBanks.keys.collect { |nBank|
  "<button onclick='on_bank(0, #{nBank})'>BANK #{nBank}</button>"
}.join(" ")
aHtml << sBanks;
hFxBanks.each { |nBank, hBank|
  sDisplay = (nBank == 0) ? 'block' : 'none';
  aHtml << "<div id='bank-0-#{nBank}' style='display: #{sDisplay}'>";
  hBank.each { |sType, hType|
    aHtml << '<table>';
    hType.each { |sCtrl, hCtrl|
      aHtml << "<tr>";
      aHtml << "<td colspan='8' class='#{sType}-header'>[#{nBank}] - #{sType.upcase} - #{sCtrl.upcase}</td>";
      aHtml << "</tr>";
      hCtrl.each { |sRow, aRow|
        aHtml << '<tr>';
        aRow.each { |sCell|
          if (sCell == nil)
            aHtml << '<td></td>';
          else
            aHtml << sCell;
          end
        }
        aHtml << '</tr>';
      }
    }
    aHtml << '</table>';
  }
  aHtml << '</div>';
}
aHtml << sBanks;
aHtml << '</div>';

nInst = 1;
hInsBanks.each { |sInstrument, aBanks|
  aHtml << "<div id='group-#{nInst}' style='display: none'>";
  sBanks = Range.new(0, aBanks.length - 1).collect { |nIdx|
    "<button onclick='on_bank(#{nInst}, #{nIdx})'>BANK #{nIdx}</button>";
  }
  aHtml << sBanks;
  nBank = 0
  aBanks.each { |hBank|
    sDisplay = (nBank == 0) ? 'block' : 'none';
    aHtml << "<div id='bank-#{nInst}-#{nBank}' style='display: #{sDisplay}'>";
    hBank.each { |sType, hType|
      aHtml << '<table>';
      hType.each { |sCtrl, hCtrl|
        aHtml << "<tr>";
        aHtml << "<td colspan='8' class='#{sType}-header'>[#{nBank}] - #{sType.upcase} - #{sCtrl.upcase}</td>";
        aHtml << "</tr>";
        hCtrl.each { |sRow, aRow|
          aHtml << '<tr>';
          aRow.each { |sCell|
            if (sCell == nil)
              aHtml << '<td></td>';
            else
              aHtml << sCell;
            end
          }
          aHtml << '</tr>';
        }
      }
      aHtml << '</table>';
    }
    nBank += 1;
    aHtml << '</div>';
  }
  aHtml << sBanks;
  aHtml << '</div>';
  nInst += 1;
}

aHtml << aMenu;
aHtml << '</body>';

oFile = File.new("banks.html", "wt");
oFile.puts(aHtml.join("\n"))

