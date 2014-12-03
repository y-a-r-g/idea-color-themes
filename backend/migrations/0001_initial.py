# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Theme'
        db.create_table(u'backend_theme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('elements', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('downloads', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True)),
            ('ect', self.gf('django.db.models.fields.IntegerField')(default=-1, blank=True)),
            ('promote', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(default='', max_length=2048, blank=True)),
            ('archive', self.gf('django.db.models.fields.files.FileField')(default='', max_length=260)),
            ('moderating', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'backend', ['Theme'])

        # Adding model 'ShoppingToken'
        db.create_table(u'backend_shoppingtoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='4D32MKJ9ORH6RI17WGZ8863SYPX07GGT6Z2Z9NJK2Q0D05FPKJG1GXNUNQIW92YQUA58UPRO3KDMMLCOHVSHPQYA4CMWXIXM', max_length=127, blank=True)),
            ('payed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'backend', ['ShoppingToken'])


    def backwards(self, orm):
        # Deleting model 'Theme'
        db.delete_table(u'backend_theme')

        # Deleting model 'ShoppingToken'
        db.delete_table(u'backend_shoppingtoken')


    models = {
        u'backend.shoppingtoken': {
            'Meta': {'object_name': 'ShoppingToken'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "'T48FO1UF6O9L84HD7LTXLA6SGO72Y3O8KAHLI08U3RNVLWV7U811J2JZKPXMA5U2W3N1WIVEE46Y7H2U75JO4H9V1RN7D6JR'", 'max_length': '127', 'blank': 'True'})
        },
        u'backend.theme': {
            'Meta': {'object_name': 'Theme'},
            'archive': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '260'}),
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '2048', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'downloads': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'ect': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'blank': 'True'}),
            'elements': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderating': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'promote': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'})
        }
    }

    complete_apps = ['backend']