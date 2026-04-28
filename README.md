<div align="center">

<img src="https://img.shields.io/badge/-DSAN%205200-008cba?style=for-the-badge&logoColor=white" alt="DSAN 5200"/>
&nbsp;
<img src="https://img.shields.io/badge/Georgetown%20University-041E42?style=for-the-badge&logoColor=white" alt="Georgetown University"/>
&nbsp;
<img src="https://img.shields.io/badge/Spring%202026-008cba?style=for-the-badge&logoColor=white" alt="Spring 2026"/>

<br/><br/>

<h1>The Way Flight Pricing Works is Unfair</h1>

<p><em>A data-driven narrative on airline fare inequality in the US domestic market</em></p>

<p>
  <strong>Akshay Arun &nbsp;·&nbsp; Alexa Nakanishi &nbsp;·&nbsp; Norman Wang</strong>
</p>

<a href="https://normanw.georgetown.domains/airlines-data-viz/report/report.html">
  <img src="https://img.shields.io/badge/View%20Report-008cba?style=for-the-badge&logoColor=white" alt="View Report"/>
</a>


&nbsp;
<a href="https://5200-data-viz.streamlit.app/">
  <img src="https://img.shields.io/badge/Flight%20Exploration%20&%20Recommendation%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Flight Recommendation App"/>
</a>

</div>

---

## About

This project analyzes US domestic airline pricing using BTS DB1B Market data spanning **Q3 2024 – Q2 2025** (25M+ records). Our central finding: distance alone does not explain what you pay. Market structure and carrier concentration play a significant role in driving fares higher.

---

## Assessed Factors

<div align="center">
<br/>

<table cellpadding="20">
  <tr>
    <td align="center" bgcolor="#008cba" width="210">
      <strong><font color="#ffffff">Distance</font></strong>
      <br/><br/>
      <font color="#d6f0f8">How far you fly between origin and destination</font>
    </td>
    <td width="20"></td>
    <td align="center" bgcolor="#008cba" width="210">
      <strong><font color="#ffffff">Market Competition</font></strong>
      <br/><br/>
      <font color="#d6f0f8">How many carriers serve a route and how concentrated their market share</font>
    </td>
    <td width="20"></td>
    <td align="center" bgcolor="#008cba" width="210">
      <strong><font color="#ffffff">Intermediary Carriers</font></strong>
      <br/><br/>
      <font color="#d6f0f8">Having Operating vs. Ticket carrier companies in the flight-purchasing processing</font>
    </td>
  </tr>
</table>

<br/>
</div>

---

## Data Sources

| Dataset | Description |
|---|---|
| **BTS DB1B Market Survey** | Q3 2024 – Q2 2025 · Origin–destination fare and itinerary data |
| **BTS Form 41 P6** | Carrier financial statistics |
| **BTS T100 Segment Data** | Domestic segment-level traffic and capacity |
| **OurAirports** | Airport latitude / longitude coordinates |

> Raw data files are git-ignored due to size.
