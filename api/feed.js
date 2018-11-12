
/*
Copyright (c) 2018-present, Taatu Ltd.

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*/
const express = require('express')
const app = express()
const port = 8888
require('../../sa_pwd/sa_access.js')();

app.get('/feed', function (req, res) {

  var m = req.query.m;
  var a = req.query.a;
  var q = ''

  if (m) {
    q = m
  }

  if (a) {
    q = a
  }

  var mysql = require('mysql');

  var con = mysql.createConnection({
    host: sahost(),
    user: sausername(),
    password: sapassword(),
    database: sadatabase()
  });


  con.connect(function(err) {
    if (err) throw err;
    con.query("SELECT * FROM feed WHERE search LIKE '%"+q+"%' ORDER BY date DESC", function (err, result, fields) {
      if (err) throw err;
        res.send(result)
    });
  });


})

app.listen(port, () => console.log(`Listening on port ${port}!`))
